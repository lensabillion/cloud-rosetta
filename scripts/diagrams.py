#!/usr/bin/env python3
"""One diagram source for standalone SVG, GitHub chapters and the web guide.

Notation follows docs/architecture.md: labelled scope boundaries, explicit
relationship types, real service names, and readable text instead of icon guesses.
"""
from __future__ import annotations

from dataclasses import dataclass
import html
import pathlib
import textwrap
import architecture_art

WIDTH = 960
import design as _design

# Standalone SVG files cannot read the page's CSS custom properties, so the
# values are inlined here. They are read from data/design.yml rather than
# written down twice, which is how this palette had drifted to the previous
# design without anyone noticing.
_TOKENS = _design.load()["colour"]["light"]
PALETTE = {
    'aws': _TOKENS['aws'], 'azure': _TOKENS['azure'], 'gcp': _TOKENS['gcp'],
    'neutral': _TOKENS['ink2'],
}
NEUTRAL = _TOKENS['ink2']
SURFACE = _TOKENS['sheet']
BOUNDARY_FILL = _TOKENS['sunk']


def esc(value: str) -> str:
    return html.escape(str(value), quote=True)


@dataclass
class Diagram:
    name: str
    title: str
    description: str
    height: int
    parts: list[str]

    def text(self, x, y, value, width=48, size=15, color=NEUTRAL, bold=False):
        lines = textwrap.wrap(value, width, break_long_words=False, break_on_hyphens=False)
        self.parts.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" '
                          f'font-weight="{700 if bold else 400}">')
        for i, line in enumerate(lines):
            self.parts.append(f'<tspan x="{x}" dy="{0 if i == 0 else 21}">{esc(line)}</tspan>')
        self.parts.append('</text>')

    def box(self, x, y, w, h, title, detail='', color='neutral', boundary=False):
        hue = PALETTE[color]
        dash = ' stroke-dasharray="7 5"' if boundary else ''
        fill = BOUNDARY_FILL if boundary else SURFACE
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" '
                          f'fill="{fill}" stroke="{hue}" stroke-width="1.5"{dash}/>')
        self.text(x+14, y+24, title, max(12, int((w-28)/8)), color=hue, bold=True)
        if detail:
            title_lines = len(textwrap.wrap(title, max(12, int((w-28)/8)), break_long_words=False, break_on_hyphens=False))
            self.text(x+14, y+47+21*(title_lines-1), detail, max(12, int((w-28)/7.5)), size=14)

    def arrow(self, x1, y1, x2, y2, label, control=False):
        dash = ' stroke-dasharray="5 4"' if control else ''
        self.parts.append(f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="{NEUTRAL}" '
                          f'stroke-width="1.8" marker-end="url(#{self.name}-arrow)"{dash}/>')
        # Labels use their own white strip so they never collide with a line.
        lx, ly = (x1+x2)/2, (y1+y2)/2
        length = len(label)*7.2+14
        self.parts.append(f'<rect x="{lx-length/2}" y="{ly-12}" width="{length}" height="21" fill="#fff"/>')
        self.parts.append(f'<text x="{lx}" y="{ly+3}" text-anchor="middle" font-size="14" fill="{NEUTRAL}">{esc(label)}</text>')

    def svg(self):
        header = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {self.height}" '
                  f'role="img" aria-labelledby="{self.name}-title {self.name}-desc" '
                  'font-family="Arial, Helvetica, sans-serif">'
                  f'<title id="{self.name}-title">{esc(self.title)}</title>'
                  f'<desc id="{self.name}-desc">{esc(self.description)}</desc>'
                  f'<defs><marker id="{self.name}-arrow" viewBox="0 0 10 10" refX="9" refY="5" '
                  f'markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{NEUTRAL}"/></marker></defs>'
                  f'<rect width="960" height="{self.height}" fill="#fff"/>')
        return header + ''.join(self.parts) + '</svg>\n'


def canvas(name, title, description, height=620):
    d = Diagram(name, title, description, height, [])
    d.text(24, 34, title, width=70, size=23, bold=True)
    d.text(24, 61, 'Cloud Rosetta | Conceptual architecture | Sources and assumptions in the chapter', width=110, size=14)
    d.text(24, height-42, 'Legend: dashed box = labelled scope; solid arrow = named relationship;', width=115, size=14)
    d.text(24, height-21, 'dashed arrow = control or recovery action. Colors identify providers, not security.', width=115, size=14)
    return d


def hierarchy():
    d=canvas('hierarchy','Administrative ownership is not geography',
              'Administrative parentage only. Optional OUs, management groups and folders group workload boundaries. Regions and zones are not children in this tree.',680)
    chains=[('aws','AWS',['Organization root','OU (optional)','Account','Workload resources']),
            ('azure','Azure',['Root management group','Management group (optional)','Subscription','Resource group','Resources at this scope']),
            ('gcp','Google Cloud',['Organization','Folder (optional)','Project','Workload resources'])]
    for col,(key,label,nodes) in enumerate(chains):
        x=24+col*312
        d.box(x,88,288,520,label,color=key,boundary=True)
        for i,node in enumerate(nodes):
            y=130+i*92
            d.box(x+14,y,260,54,node,color=key)
            if i: d.arrow(x+144,y-38,x+144,y,'parent of')
    return d


def scope():
    d=canvas('scope','Network membership and location are separate',
              'Each subnet belongs to its virtual network. AWS subnets occupy one zone; Azure and Google subnets are regional. A network does not own geographic zones.',490)
    values=[('aws','AWS','VPC','Regional','Subnet','One Availability Zone'),
            ('azure','Azure','Virtual network','Regional','Subnet','Regional; not zone-bound'),
            ('gcp','Google Cloud','VPC network','Global','Subnet','One region')]
    for col,(key,label,network,location,subnet,subplace) in enumerate(values):
        x=24+312*col
        d.box(x,90,288,314,label,color=key,boundary=True)
        d.box(x+16,138,256,82,network,'Location: '+location,color=key)
        d.arrow(x+144,220,x+144,274,'contains subnet')
        d.box(x+16,274,256,104,subnet,'Location: '+subplace,color=key)
    return d


def role():
    d=canvas('role','Identity, credentials and permissions',
              'AWS STS issues temporary role-session credentials after successful role assumption. Azure RBAC and Google IAM assign a permission set to a principal at a scope; conditions and denies still apply.',550)
    d.text(24,106,'AWS | role assumption and an authorized request',width=90,bold=True)
    d.box(24,126,230,90,'Principal','User, workload or federation')
    d.box(364,126,230,90,'Role session','Temporary STS credentials',color='aws')
    d.box(704,126,230,90,'Target resource','Checks applicable policies',color='aws')
    d.arrow(254,171,364,171,'assume role')
    d.arrow(594,171,704,171,'API request')
    d.text(24,265,'Trust policy controls who may assume the role; an assumption request must be authorized.',width=112,size=14)
    d.text(24,325,'Azure / Google | a grant relates a principal, a permission set and a scope',width=100,bold=True)
    d.box(24,350,230,92,'Principal','Person or workload')
    d.box(364,350,230,92,'Role assignment / binding','Role is a permission set')
    d.box(704,350,230,92,'Scope','Grant can inherit to children')
    d.arrow(254,396,364,396,'receives grant',control=True)
    d.arrow(594,396,704,396,'applies at',control=True)
    return d


def decision():
    d=canvas('identity-decision','Two bounded AWS permission decisions',
              'Example A: identity allows PutObject but boundary allows only GetObject, so deny. Example B: same-account bucket policy directly grants an IAM user GetObject, so omission from identity policy and boundary alone does not block it. No other restrictions are assumed.',470)
    for x,title,grant,restriction,outcome in [
        (24,'A | Identity-based grant','User policy allows PutObject','Boundary permits only GetObject','DENIED'),
        (504,'B | Direct resource grant','Bucket grants user ARN GetObject','Identity and boundary omit it','ALLOWED under stated assumptions')]:
        d.box(x,94,432,276,title,color='aws',boundary=True)
        d.text(x+18,155,grant,width=48,bold=True)
        d.text(x+18,195,restriction,width=48)
        d.text(x+18,266,outcome,width=44,bold=True)
        d.text(x+18,311,'No applicable explicit deny or other restricting control.',width=48,size=14)
    return d


def firewall():
    d=canvas('firewall','Native network filtering: specify the control',
              'AWS security groups are stateful allow-only while network ACLs are stateless allow/deny. Azure NSGs are stateful at subnet or NIC. Google VPC firewall rules belong to a network and target VM interfaces.',570)
    items=[('aws','AWS','Network ACL | subnet','Stateless; allow and deny','Security group | interface','Stateful; allow only'),
           ('azure','Azure','NSG | subnet','Stateful; allow and deny','NSG | network interface','If both are assigned, both apply'),
           ('gcp','Google Cloud','VPC firewall rule','Defined on the VPC network','VM interface targets','All instances, tags or service accounts')]
    for col,(key,label,a,aa,b,bb) in enumerate(items):
        x=24+col*312
        d.box(x,94,288,385,label,color=key,boundary=True)
        d.box(x+16,147,256,102,a,aa,color=key)
        d.box(x+16,304,256,112,b,bb,color=key)
        d.text(x+16,447,'See chapter for defaults and priority.',width=33,size=14)
    return d


def multiaz():
    d=canvas('multiaz','RDS: availability and readable replicas',
              'A Multi-AZ DB instance has a synchronous unreadable standby. A Multi-AZ DB cluster has semisynchronous replication to two readable standbys in three zones. An ordinary read replica uses asynchronous replication and is not automatic failover for its source.',650)
    panels=[('DB instance','Primary | AZ A','Standby | AZ B','Synchronous','Standby does not serve reads'),
            ('DB cluster','Writer | AZ A','Reader | AZ B','Semisynchronous','Also reader in AZ C; both readable'),
            ('Ordinary read replica','Source database','Read replica','Asynchronous','No automatic source failover')]
    for i,(title,a,b,label,caption) in enumerate(panels):
        x=24+312*i
        d.box(x,94,288,454,title,color='aws',boundary=True)
        d.box(x+16,146,256,60,a,color='aws')
        d.arrow(x+144,206,x+144,277,label)
        d.box(x+16,277,256,60,b,color='aws')
        if i==1:
            d.box(x+16,394,256,60,'Reader | AZ C',color='aws')
            # Both readers receive the writer's log, not a chain of reader replication.
            d.parts.append(f'<path d="M{x+270},176 L{x+280},176 L{x+280},424 L{x+272},424" fill="none" stroke="{NEUTRAL}" marker-end="url(#multiaz-arrow)"/>')
        d.text(x+16,489,caption,width=31,size=14)
    return d


def failover():
    d=canvas('database-failover','RDS DB instance: before and after a zone outage',
              'Before failure the database endpoint directs clients to the primary in zone A, with synchronous replication to a non-readable standby in zone B. After RDS promotes the standby, clients reconnect using the endpoint; existing sessions are interrupted.',560)
    for x,after in [(24,False),(504,True)]:
        d.box(x,94,432,368,'AFTER failover' if after else 'BEFORE outage',color='aws',boundary=True)
        d.box(x+104,140,224,70,'Application','Uses DB endpoint; retries safely')
        d.box(x+14,323,194,90,'AZ A','Unavailable' if after else 'Primary: reads / writes',color='aws')
        d.box(x+224,323,194,90,'AZ B','Promoted: reads / writes' if after else 'Standby: no client reads',color='aws')
        d.arrow(x+216,210,x+(321 if after else 111),323,'reconnect' if after else 'SQL session',control=after)
        if not after:d.arrow(x+208,369,x+224,369,'sync')
    return d


def private_access():
    d=canvas('private-access','Private endpoints: the service stays outside your subnet',
              'Consumer clients connect to a private endpoint in their network, which connects to a supported provider service outside that consumer network. AWS interface endpoints, Azure private endpoints and Google PSC endpoints need correct DNS, routes and permissions.',650)
    for i,(key,label,endpoint) in enumerate([('aws','AWS','Interface endpoint'),('azure','Azure','Private endpoint'),('gcp','Google Cloud','PSC endpoint')]):
        x=24+i*312
        d.box(x,94,288,296,label+' | consumer network',color=key,boundary=True)
        d.box(x+16,142,256,64,'Client workload','Resolve service name')
        d.arrow(x+144,206,x+144,277,'private destination')
        d.box(x+16,277,256,86,endpoint,'Private IP / endpoint interface',color=key)
        d.arrow(x+144,363,x+144,459,'service connection')
        d.box(x+16,459,256,90,'Supported service','Provider-managed boundary',color=key)
    return d


def responsibility():
    d=canvas('responsibility','Managed service does not mean unmanaged responsibility',
              'Customer duties remain across IaaS, PaaS and SaaS: protect data, manage access and configure available controls. Guest OS management is normally customer responsibility in IaaS and provider responsibility in managed PaaS and SaaS. Service-specific shared duties remain.',490)
    for i,(model,detail) in enumerate([('IaaS','Operate guest OS and applications'),('PaaS','Configure application and platform controls'),('SaaS','Configure service settings and access')]):
        x=24+i*312
        d.box(x,94,288,304,model,boundary=True)
        d.box(x+16,148,256,100,'Customer duties remain','Data protection, identities, access and available settings')
        d.box(x+16,279,256,88,'Service-dependent duties',detail)
    return d




ALL={
    'deployment-aws':lambda:architecture_art.render('deployment-aws'),
    'deployment-azure':lambda:architecture_art.render('deployment-azure'),
    'deployment-gcp':lambda:architecture_art.render('deployment-gcp'),
    'hierarchy':hierarchy,'scope':scope,'role':role,'identity-decision':decision,
    'firewall':firewall,'multiaz':multiaz,'database-failover':failover,
    'private-access':private_access,'responsibility':responsibility,
    'application-aws':lambda:architecture_art.render('application-aws'),
    'application-azure':lambda:architecture_art.render('application-azure'),
    'application-gcp':lambda:architecture_art.render('application-gcp'),
}


def render(name: str, instance: str = "") -> str:
    if name not in ALL:
        raise ValueError(f'Unknown diagram: {name}')
    drawing=ALL[name]()
    instance = instance or name
    svg = drawing.svg().replace(name + "-", instance + "-")
    figure_class = "fig service-architecture" if isinstance(drawing, architecture_art.ArchitectureDrawing) else "fig"
    return (f'<figure class="{figure_class}" id="fig-{instance}"><div class="diagram-scroll" tabindex="0" '
            f'role="region" aria-label="{esc(drawing.title)}; scroll horizontally on small screens">'
            + svg + '</div>'
            + f'<figcaption>{esc(drawing.description)} '
            + f'<a href="assets/architecture/{name}.svg">Open full-size SVG</a></figcaption></figure>')


def export(root: pathlib.Path) -> None:
    for base in (root/'docs/assets/architecture', root/'site/assets/architecture'):
        base.mkdir(parents=True,exist_ok=True)
        for name,factory in ALL.items():
            (base/f'{name}.svg').write_text(factory().svg(),encoding='utf-8')
