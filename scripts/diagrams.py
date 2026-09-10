#!/usr/bin/env python3
"""Inline SVG diagrams for the guide.

Each one exists to show a mechanism the prose cannot: what contains what, where
a filter attaches, what you become when you assume a role. Structure is drawn in
currentColor so it follows the theme; the three provider hues are the one place
a literal colour carries meaning, and they come from the page's own tokens.

Referenced from a chapter with an HTML comment: <!-- diagram: hierarchy -->
"""

from __future__ import annotations

ARROW = """<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5"
markerWidth="6" markerHeight="6" orient="auto-start-reverse">
<path d="M0,0 L10,5 L0,10 z" fill="currentColor"/></marker></defs>"""

HUE = {"aws": "var(--aws)", "azure": "var(--azure)", "gcp": "var(--gcp)"}


def figure(name: str, claim: str, w: int, h: int, body: str, caption: str) -> str:
    return (
        f'<figure class="fig" id="fig-{name}">'
        f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{claim}">{ARROW}{body}</svg>'
        f"<figcaption>{caption}</figcaption></figure>"
    )


def box(x, y, w, h, label, sub=None, hue=None, dash=False, weight=400):
    stroke = HUE[hue] if hue else "currentColor"
    d = ' stroke-dasharray="4 4"' if dash else ""
    op = ' opacity=".55"' if dash else ""
    out = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="none" '
           f'style="stroke:{stroke}"{d}{op}/>')
    ty = y + 17
    out += (f'<text x="{x + 11}" y="{ty}" font-size="13" font-weight="{weight}" '
            f'style="fill:{stroke if hue else "currentColor"}">{label}</text>')
    if sub:
        out += (f'<text x="{x + 11}" y="{ty + 16}" font-size="12" opacity=".62" '
                f'fill="currentColor">{sub}</text>')
    return out


def tag(x, y, text, hue=None):
    fill = HUE[hue] if hue else "currentColor"
    return (f'<text x="{x}" y="{y}" font-size="11" text-anchor="end" '
            f'style="fill:{fill}" opacity=".9" font-weight="600">{text}</text>')


def title(x, y, text, hue):
    return (f'<text x="{x}" y="{y}" font-size="13" font-weight="700" '
            f'letter-spacing=".08em" style="fill:{HUE[hue]}">{text.upper()}</text>')


def arrow(x1, y1, x2, y2, label=None, dash=False, above=True):
    d = ' stroke-dasharray="5 4"' if dash else ""
    out = (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="currentColor" '
           f'stroke-width="1.4"{d} marker-end="url(#ar)"/>')
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2 + (-7 if above else 15)
        out += (f'<text x="{mx}" y="{my}" font-size="12" text-anchor="middle" '
                f'fill="currentColor" opacity=".75">{label}</text>')
    return out


def note(x, y, text, anchor="start"):
    return (f'<text x="{x}" y="{y}" font-size="12" text-anchor="{anchor}" '
            f'fill="currentColor" opacity=".65">{text}</text>')


# --------------------------------------------------------------------------- 1

def hierarchy() -> str:
    b = title(20, 20, "AWS", "aws") + title(316, 20, "Azure", "azure") + title(612, 20, "Google Cloud", "gcp")

    # AWS: one object carries all three jobs
    b += box(20, 34, 268, 286, "Organization", hue="aws", dash=True)
    b += box(34, 66, 240, 244, "Organizational unit", dash=True)
    b += box(48, 98, 212, 202, "Account", "isolation + billing + identity", hue="aws", weight=700)
    b += box(62, 146, 184, 144, "Region")
    b += box(76, 178, 156, 102, "VPC", "regional")
    b += box(90, 226, 128, 44, "Availability Zone", "holds the subnet")

    # Azure: identity, billing and lifecycle are three different objects
    b += box(316, 34, 268, 286, "Entra ID tenant", "identity", hue="azure", dash=True)
    b += box(330, 82, 240, 228, "Management group", dash=True)
    b += box(344, 114, 212, 186, "Subscription", "billing", hue="azure", weight=700)
    b += box(358, 162, 184, 128, "Resource group", "mandatory, deletes contents")
    b += box(372, 210, 156, 68, "Virtual network", "regional, subnets span zones")

    # Google: the network escapes the region entirely
    b += box(612, 34, 268, 210, "Organization", hue="gcp", dash=True)
    b += box(626, 66, 240, 164, "Folder", dash=True)
    b += box(640, 98, 212, 118, "Project", "isolation boundary", hue="gcp", weight=700)
    b += box(654, 146, 184, 56, "Region", "holds the subnet")
    b += box(626, 258, 240, 62, "VPC network", "global, outside every region", hue="gcp", weight=700)
    b += arrow(746, 258, 746, 232, dash=True)

    return figure(
        "hierarchy",
        "The containment hierarchy of AWS, Azure and Google Cloud drawn side by side at the same scale",
        900, 336, b,
        "One object or three. An AWS account is the isolation, billing and identity boundary at once; "
        "Azure splits those across a tenant, a subscription and a resource group. Only Google's network "
        "sits outside the region, which is why one Google VPC spans every region while an AWS subnet "
        "sits inside a single zone.",
    )


# --------------------------------------------------------------------------- 2

def scope() -> str:
    lanes = [("Global", 46), ("Regional", 106), ("Zonal", 166)]
    b = ""
    for label, y in lanes:
        b += f'<line x1="120" y1="{y + 22}" x2="840" y2="{y + 22}" stroke="currentColor" opacity=".16"/>'
        b += (f'<text x="108" y="{y + 16}" font-size="12" font-weight="700" text-anchor="end" '
              f'fill="currentColor" opacity=".8">{label}</text>')

    cols = {"aws": 150, "azure": 400, "gcp": 650}
    for k, x in cols.items():
        b += title(x, 26, {"aws": "AWS", "azure": "Azure", "gcp": "Google Cloud"}[k], k)

    def chip(x, y, text, hue, strong=False):
        w = max(96, 8 + len(text) * 6.4)
        return (f'<rect x="{x}" y="{y}" width="{w}" height="26" rx="13" fill="none" '
                f'style="stroke:{HUE[hue]}" stroke-width="{2 if strong else 1}"/>'
                f'<text x="{x + w / 2}" y="{y + 17}" font-size="12" text-anchor="middle" '
                f'font-weight="{700 if strong else 400}" style="fill:{HUE[hue]}">{text}</text>')

    b += chip(150, 106, "VPC", "aws") + chip(150, 166, "Subnet", "aws", True)
    b += chip(400, 106, "VNet", "azure") + chip(400, 106 + 32, "Subnet", "azure")
    b += chip(650, 46, "VPC network", "gcp", True) + chip(650, 106, "Subnet", "gcp")
    b += chip(150, 166 + 32, "Instance", "aws") + chip(400, 166, "Instance", "azure") + chip(650, 166, "Instance", "gcp")

    return figure(
        "scope",
        "Where the virtual network and subnet live on the global, regional and zonal scale in each cloud",
        880, 214, b,
        "The two rows that decide questions. A Google VPC is global; an AWS subnet is zonal. Azure sits "
        "between the two, with a regional network and regional subnets that span the zones.",
    )


# --------------------------------------------------------------------------- 3

def role() -> str:
    b = '<text x="20" y="18" font-size="13" font-weight="700" letter-spacing=".08em" fill="currentColor">AWS &#183; YOU BECOME IT</text>'
    b += box(20, 34, 130, 46, "User", "or service")
    b += arrow(150, 57, 236, 57, "assumes")
    b += box(236, 26, 178, 62, "IAM role", "an identity, with its own temporary credentials", hue="aws", weight=700)
    b += arrow(414, 57, 500, 57, "acts as")
    b += box(500, 34, 130, 46, "Resource")
    b += note(236, 106, "The role holds a trust policy naming who may assume it.")

    b += '<line x1="20" y1="132" x2="860" y2="132" stroke="currentColor" opacity=".18"/>'
    b += '<text x="20" y="160" font-size="13" font-weight="700" letter-spacing=".08em" fill="currentColor">AZURE AND GOOGLE &#183; IT IS PINNED TO YOU</text>'
    b += box(20, 176, 130, 46, "User", "or group")
    b += box(236, 176, 178, 46, "Role", "a list of permissions, no credentials", hue="azure", weight=700)
    b += arrow(150, 199, 236, 199, "granted")
    b += arrow(414, 199, 500, 199, "at a scope")
    b += box(500, 168, 150, 62, "Scope", "subscription, project, resource group", hue="gcp", weight=700)
    b += arrow(575, 230, 575, 258, "inherits down")
    b += box(500, 258, 150, 34, "Everything beneath it")
    b += note(20, 286, "Grants are additive. A narrower role lower down removes nothing.")

    return figure(
        "role",
        "An AWS role is an identity you assume, while an Azure or Google role is a permission set granted to somebody else at a scope",
        880, 306, b,
        "The same word, two different kinds of object. In AWS you become the role and receive its "
        "credentials. In Azure and Google the role is a list of verbs pinned to a separate principal at a "
        "place, and everything under that place inherits it.",
    )


# --------------------------------------------------------------------------- 4

def firewall() -> str:
    b = title(20, 18, "AWS", "aws") + title(310, 18, "Azure", "azure") + title(600, 18, "Google Cloud", "gcp")

    b += box(20, 30, 262, 172, "VPC", hue="aws", dash=True)
    b += box(32, 62, 238, 128, "Subnet")
    b += box(44, 92, 214, 42, "Network ACL", "stateless, allow and deny", hue="aws", weight=700)
    b += box(44, 144, 214, 36, "Security group on the interface", hue="aws", weight=700)
    b += note(32, 218, "Two layers. Only the ACL can deny.")

    b += box(310, 30, 262, 172, "Virtual network", hue="azure", dash=True)
    b += box(322, 62, 238, 128, "Subnet")
    b += box(334, 92, 214, 36, "NSG on the subnet", hue="azure", weight=700)
    b += box(334, 138, 214, 42, "NSG on the interface", "both apply, in order", hue="azure", weight=700)
    b += note(322, 218, "Same object, either level, or both.")

    b += box(600, 30, 262, 172, "VPC network", "the rules live here", hue="gcp", dash=True, weight=700)
    b += box(612, 76, 238, 40, "Firewall rule", hue="gcp", weight=700)
    b += arrow(731, 116, 731, 146, "selects by tag")
    b += box(612, 146, 238, 40, "Instances carrying that tag")
    b += note(612, 218, "Nothing attaches to the machine itself.")

    return figure(
        "firewall",
        "Where traffic filtering attaches in each cloud: the interface and subnet in AWS, either level in Azure, and the network itself in Google Cloud",
        880, 232, b,
        "The attachment point is the difference. Google's rules belong to the network and reach instances "
        "by tag, so an engineer arriving from AWS looks for a firewall on the machine and does not find "
        "one. And only the AWS network ACL can express a deny.",
    )


# --------------------------------------------------------------------------- 5

def multiaz() -> str:
    b = '<text x="20" y="16" font-size="13" font-weight="700" fill="currentColor">Multi-AZ DB instance</text>'
    b += box(20, 28, 116, 44, "Primary", "zone a", hue="aws")
    b += arrow(136, 50, 196, 50, "synchronous")
    b += box(196, 28, 116, 44, "Standby", "zone b")
    b += note(20, 92, "Standby serves no reads. It exists to fail over.")

    b += '<line x1="0" y1="112" x2="880" y2="112" stroke="currentColor" opacity=".18"/>'
    b += '<text x="20" y="140" font-size="13" font-weight="700" fill="currentColor">Multi-AZ DB cluster</text>'
    b += box(20, 152, 116, 44, "Writer", "zone a", hue="aws")
    b += arrow(136, 174, 196, 174, "synchronous")
    b += box(196, 152, 116, 44, "Reader", "zone b", hue="aws")
    b += box(332, 152, 116, 44, "Reader", "zone c", hue="aws")
    b += note(20, 216, "Readers serve reads and can be promoted.")

    b += '<line x1="0" y1="236" x2="880" y2="236" stroke="currentColor" opacity=".18"/>'
    b += '<text x="20" y="264" font-size="13" font-weight="700" fill="currentColor">Read replica</text>'
    b += box(20, 276, 116, 44, "Primary", hue="aws")
    b += arrow(136, 298, 196, 298, "asynchronous", dash=True)
    b += box(196, 276, 116, 44, "Replica", "readable")
    b += note(20, 340, "Scales reads. Does not fail over on its own.")

    b += '<line x1="470" y1="24" x2="470" y2="348" stroke="currentColor" opacity=".18"/>'
    b += '<text x="496" y="46" font-size="13" font-weight="700" fill="currentColor">Pick by the constraint</text>'
    b += note(496, 74, "“Survive a zone failure”  →  a Multi-AZ deployment")
    b += note(496, 100, "“Reporting must not slow the app”  →  a read replica")
    b += note(496, 126, "“Both, from one deployment”  →  a Multi-AZ cluster")
    b += note(496, 168, "The blanket rule “a standby is never readable”")
    b += note(496, 190, "is true of the instance form only.")

    return figure(
        "multiaz",
        "Multi-AZ DB instance, Multi-AZ DB cluster and read replica compared by what each one can serve and what it does on failure",
        880, 360, b,
        "Three deployments that a single sentence about Multi-AZ flattens. Whether the standby answers "
        "reads depends on which one you chose, so a question about it is underspecified until the "
        "deployment type is named.",
    )


# --------------------------------------------------------------------------- 6

def responsibility() -> str:
    layers = ["Applications", "Data", "Runtime", "Operating system", "Virtualisation",
              "Servers and storage", "Networking and facilities"]
    cols = [("On premises", 7), ("IaaS", 4), ("PaaS", 2), ("SaaS", 0)]
    x0, w, rh = 210, 150, 32
    b = ""
    for i, layer in enumerate(layers):
        y = 52 + i * rh
        b += (f'<text x="{x0 - 16}" y="{y + 20}" font-size="12" text-anchor="end" '
              f'fill="currentColor" opacity=".8">{layer}</text>')

    for c, (name, yours) in enumerate(cols):
        cx = x0 + c * (w + 8)
        b += (f'<text x="{cx + w / 2}" y="34" font-size="13" font-weight="700" text-anchor="middle" '
              f'fill="currentColor">{name}</text>')
        for i in range(len(layers)):
            y = 52 + i * rh
            mine = i < yours
            fill = "currentColor" if mine else HUE["azure"]
            op = ".10" if mine else ".16"
            b += (f'<rect x="{cx}" y="{y}" width="{w}" height="{rh - 4}" rx="3" '
                  f'style="fill:{fill};stroke:{fill}" fill-opacity="{op}" stroke-opacity=".5"/>')
        if yours:
            b += (f'<line x1="{cx}" y1="{52 + yours * rh - 2}" x2="{cx + w}" y2="{52 + yours * rh - 2}" '
                  f'stroke="currentColor" stroke-width="2"/>')

    b += (f'<rect x="{x0}" y="290" width="14" height="14" rx="2" fill="currentColor" fill-opacity=".10" '
          f'stroke="currentColor" stroke-opacity=".5"/>')
    b += note(x0 + 22, 302, "you manage")
    b += (f'<rect x="{x0 + 130}" y="290" width="14" height="14" rx="2" '
          f'style="fill:{HUE["azure"]};stroke:{HUE["azure"]}" fill-opacity=".16" stroke-opacity=".5"/>')
    b += note(x0 + 152, 302, "the provider manages")

    return figure(
        "responsibility",
        "The shared responsibility line moving down the stack from on premises through IaaS and PaaS to SaaS",
        880, 318, b,
        "The same stack, four times, with the line between you and the provider in a different place. "
        "Every foundational exam asks where it sits: the provider secures the cloud, and you secure what "
        "you put in it.",
    )


ALL = {
    "hierarchy": hierarchy, "scope": scope, "role": role,
    "firewall": firewall, "multiaz": multiaz, "responsibility": responsibility,
}


def render(name: str) -> str:
    if name not in ALL:
        raise SystemExit(f"unknown diagram: {name!r}. Known: {', '.join(sorted(ALL))}")
    return ALL[name]()
