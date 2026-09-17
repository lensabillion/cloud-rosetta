"""The guide's layout and navigation follow react.dev.

A top bar with one tab per section, a sidebar tree for the current section,
breadcrumbs above each title, an outline of the page, and diagrams that scale to
the reading column instead of scrolling sideways. Built once into an isolated
folder; the developer's outputs are never rewritten.
"""
from __future__ import annotations

import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parents[1]
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr'}


class Node:
    def __init__(self, tag, attrs, parent=None):
        self.tag, self.attrs, self.parent, self.children = tag, dict(attrs), parent, []

    def classes(self):
        return (self.attrs.get('class') or '').split()

    def walk(self):
        for child in self.children:
            yield child
            yield from child.walk()

    def select(self, tag, cls=None, **attrs):
        """Descendants by tag, class and attributes; data_tree matches data-tree."""
        for node in self.walk():
            if node.tag != tag or (cls and cls not in node.classes()):
                continue
            if all(node.attrs.get(k.replace('_', '-')) == v for k, v in attrs.items()):
                yield node

    def links(self):
        return [n.attrs['href'] for n in self.walk() if n.tag == 'a' and 'href' in n.attrs]


class Tree(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = self.current = Node('#root', {})

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs, self.current)
        self.current.children.append(node)
        if tag not in VOID:
            self.current = node

    def handle_startendtag(self, tag, attrs):
        self.current.children.append(Node(tag, attrs, self.current))

    def handle_endtag(self, tag):
        node = self.current
        while node is not self.root and node.tag != tag:
            node = node.parent
        if node is not self.root:
            self.current = node.parent


class NavigationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        root = pathlib.Path(cls.temp.name)
        for name in ('scripts', 'data', 'docs'):
            shutil.copytree(ROOT / name, root / name, ignore=shutil.ignore_patterns('__pycache__'))
        shutil.copy2(ROOT / 'README.md', root / 'README.md')
        result = subprocess.run([sys.executable, 'scripts/build.py'], cwd=root,
                                capture_output=True, text=True)
        if result.returncode:
            cls.temp.cleanup()
            raise AssertionError(result.stderr)
        cls.html = (root / 'site/index.html').read_text(encoding='utf-8')
        parser = Tree()
        parser.feed(cls.html)
        cls.doc = parser.root
        cls.ids = {n.attrs['id']: n for n in cls.doc.walk() if 'id' in n.attrs}
        cls.pages = [p for p in cls.doc.select('section', cls='page') if p.attrs['id'] != 'p-home']

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def header(self):
        headers = list(self.doc.select('header', cls='topnav'))
        self.assertEqual(len(headers), 1, 'Expected one top bar')
        return headers[0]

    def tabs(self):
        return {a.attrs['data-tab']: a.attrs['href']
                for a in self.header().walk() if a.tag == 'a' and 'data-tab' in a.attrs}

    def tree(self, section):
        trees = list(self.doc.select('nav', data_tree=section))
        self.assertEqual(len(trees), 1, f'Expected one sidebar tree for {section!r}')
        return trees[0]

    def test_top_bar_has_one_tab_per_section_opening_its_first_page(self):
        tabs = self.tabs()
        self.assertEqual(list(tabs), ['learn', 'reference', 'practise'])
        for section, href in tabs.items():
            self.assertEqual(href, self.tree(section).links()[0], section)

    def test_top_bar_opens_search_and_the_menu_controls_the_sidebar(self):
        header = self.header()
        self.assertTrue([b for b in header.walk() if b.tag == 'button' and 'data-search-open' in b.attrs])
        dialogs = list(self.doc.select('dialog', cls='search'))
        self.assertEqual(len(dialogs), 1)
        self.assertTrue([n for n in dialogs[0].walk() if n.tag == 'input'])
        menu = [b for b in header.walk() if b.tag == 'button' and b.attrs.get('aria-label') == 'Menu']
        self.assertEqual(len(menu), 1)
        sidebar = self.ids[menu[0].attrs['aria-controls']]
        self.assertTrue(list(sidebar.select('nav', data_tree='learn')))

    def test_every_page_is_linked_once_from_its_section_sidebar(self):
        for page in self.pages:
            slug = page.attrs['id'][2:]
            tree = self.tree(page.attrs.get('data-section'))
            self.assertEqual(tree.links().count('#' + slug), 1, slug)

    def test_breadcrumbs_lead_back_to_the_section_before_the_title(self):
        tabs = self.tabs()
        for page in self.pages:
            slug, order = page.attrs['id'][2:], list(page.walk())
            crumbs = [n for n in order if n.tag == 'nav' and n.attrs.get('aria-label') == 'Breadcrumb']
            titles = [n for n in order if n.tag == 'h1']
            self.assertEqual((len(crumbs), len(titles)), (1, 1), slug)
            self.assertLess(order.index(crumbs[0]), order.index(titles[0]), slug)
            self.assertEqual(crumbs[0].links()[0], tabs[page.attrs['data-section']], slug)

    def test_a_nested_page_names_its_parent_in_the_breadcrumbs(self):
        parents = list(self.doc.select('li', cls='tree-parent'))
        self.assertTrue(parents)
        for parent in parents:
            parent_href = parent.links()[0]
            for href in parent.links()[1:]:
                crumbs = next(self.ids['p-' + href[1:]].select('nav', aria_label='Breadcrumb'))
                self.assertIn(parent_href, crumbs.links(), href)

    def test_page_outlines_link_only_to_their_own_page(self):
        outlines = list(self.doc.select('nav', cls='page-toc'))
        self.assertTrue(outlines)
        for outline in outlines:
            page = self.ids['p-' + outline.attrs['data-for']]
            inside = {n.attrs['id'] for n in page.walk() if 'id' in n.attrs}
            targets = [href[1:] for href in outline.links()]
            self.assertGreaterEqual(len(targets), 2)
            for target in targets:
                self.assertIn(target, inside, outline.attrs['data-for'])

    def test_a_page_with_several_sections_has_an_outline(self):
        outlined = {o.attrs['data-for'] for o in self.doc.select('nav', cls='page-toc')}
        for page in self.pages:
            sections = [n for n in page.walk() if n.tag == 'h2' and 'id' in n.attrs]
            if len(sections) >= 2:
                self.assertIn(page.attrs['id'][2:], outlined)

    def test_diagrams_scale_to_the_column_instead_of_scrolling(self):
        figures = list(self.doc.select('figure', cls='fig'))
        self.assertTrue(figures)
        for figure in figures:
            svgs = [n for n in figure.walk() if n.tag == 'svg']
            self.assertTrue(svgs and 'viewbox' in svgs[0].attrs, figure.attrs.get('id'))
            self.assertFalse([n for n in figure.walk() if 'diagram-scroll' in n.classes()])
        style = ''.join(re.findall(r'<style>(.*?)</style>', self.html, re.S))
        for selector, block in re.findall(r'([^{}]+)\{([^{}]*)\}', style):
            if '.fig' in selector:
                self.assertNotIn('min-width', block, selector.strip())
                self.assertNotRegex(block, r'overflow(-x)?:\s*(auto|scroll)', selector.strip())


if __name__ == '__main__':
    unittest.main()
