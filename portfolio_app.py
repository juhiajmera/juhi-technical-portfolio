import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Juhi Ajmera | Track Record", page_icon="📊", layout="wide")

NAVY, TEAL, GOLD, RED = "#0B2545", "#0F766E", "#B7791F", "#B42318"


def html(s):
    """Render HTML as one line so Markdown never turns indented lines into code blocks."""
    st.markdown(" ".join(line.strip() for line in s.splitlines() if line.strip()), unsafe_allow_html=True)


def section(kicker, title, sub=""):
    html(f'<div class="sec"><div class="kicker">{kicker}</div><div class="sec-title">{title}</div>'
         + (f'<div class="sec-sub">{sub}</div>' if sub else "") + "</div>")


def chips(items, cls="chip"):
    return "".join(f'<span class="{cls}">{i}</span>' for i in items)


def style_fig(fig, height=320):
    fig.update_layout(
        template="plotly_white", height=height,
        font=dict(family="Inter, Segoe UI, sans-serif", color="#334155", size=13),
        title_font=dict(size=15, color=NAVY), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=56, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.0, xanchor="right", x=1, title=None),
    )
    fig.update_xaxes(showgrid=False, linecolor="#CBD5E1")
    fig.update_yaxes(gridcolor="#E8EDF3", zeroline=False)
    return fig


html("""<style>
header[data-testid="stHeader"]{background:transparent;}
[data-testid="stMainBlockContainer"]{max-width:1240px;padding-top:2.2rem;padding-bottom:4rem;}
.hero{background:radial-gradient(1200px 400px at 85% -10%,rgba(20,184,166,.35),transparent 60%),linear-gradient(135deg,#0B2545 0%,#13315C 55%,#134E4A 100%);
 color:#fff;border-radius:20px;padding:2.6rem 2.8rem 3.6rem;box-shadow:0 18px 40px -18px rgba(11,37,69,.55);position:relative;overflow:hidden;}
.hero:after{content:"";position:absolute;right:-60px;bottom:-60px;width:260px;height:260px;border-radius:50%;border:40px solid rgba(255,255,255,.05);}
.eyebrow{text-transform:uppercase;letter-spacing:.14em;font-size:.74rem;font-weight:600;color:#99F6E4;}
.hero-name{font-size:2.9rem;font-weight:800;letter-spacing:-.02em;line-height:1.1;margin:.5rem 0 .3rem;color:#fff;}
.hero-role{font-size:1.2rem;font-weight:500;color:#CBD5E1;}
.hero-tags{margin-top:1.3rem;display:flex;flex-wrap:wrap;gap:.5rem;}
.hero-tags span{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.18);padding:.32rem .8rem;border-radius:999px;font-size:.82rem;color:#E2E8F0;}
.kpis{display:grid;grid-template-columns:repeat(5,1fr);gap:1rem;margin:-2rem 1.4rem 0;position:relative;z-index:2;}
.kpi{background:#fff;border:1px solid #E2E8F0;border-radius:14px;padding:1rem 1.1rem;box-shadow:0 8px 24px -14px rgba(15,23,42,.35);}
.kpi .v{font-size:1.9rem;font-weight:800;color:#0B2545;letter-spacing:-.02em;line-height:1.1;}
.kpi .v small{font-size:.85rem;font-weight:600;color:#0F766E;margin-left:.3rem;letter-spacing:0;}
.kpi .l{font-size:.78rem;color:#64748B;margin-top:.35rem;line-height:1.35;}
@media (max-width:900px){.kpis{grid-template-columns:repeat(2,1fr);margin:1rem 0 0;}.hero-name{font-size:2.2rem;}}
.sec{margin:2.6rem 0 1rem;}
.kicker{text-transform:uppercase;letter-spacing:.14em;font-size:.72rem;font-weight:700;color:#0F766E;}
.sec-title{font-size:1.55rem;font-weight:700;color:#0B2545;letter-spacing:-.01em;margin-top:.2rem;}
.sec-sub{color:#64748B;font-size:.95rem;margin-top:.25rem;}
.card{background:#fff;border:1px solid #E2E8F0;border-radius:14px;padding:1.3rem 1.4rem;box-shadow:0 1px 2px rgba(15,23,42,.04);height:100%;}
.card h4{margin:0 0 .6rem;font-size:.78rem;text-transform:uppercase;letter-spacing:.12em;color:#64748B;font-weight:700;padding:0;}
.summary{font-size:1.02rem;line-height:1.65;color:#334155;}
.summary b{color:#0B2545;}
.profile-card{min-height:250px;display:flex;flex-direction:column;justify-content:center;}
.profile-summary .summary-lead{font-size:1.35rem;line-height:1.45;font-weight:650;color:#0B2545;letter-spacing:-.015em;margin-bottom:.8rem;}
.profile-summary .summary-copy{font-size:.98rem;line-height:1.65;color:#475569;}
.profile-cert .cert-grid{display:flex;flex-wrap:wrap;gap:.6rem;margin:.45rem 0 0;}
.profile-cert .cert-grid span{background:#F0FDFA;border:1px solid #B8EDE3;color:#115E59;padding:.42rem .72rem;border-radius:10px;font-size:.79rem;font-weight:650;}
.skill-legend-card{background:#fff;border:1px solid #DCE4EF;border-radius:14px;padding:1.15rem 1.05rem;box-shadow:0 5px 18px -14px rgba(15,23,42,.25);position:sticky;top:1.2rem;}
.skill-legend-title{font-size:1.05rem;font-weight:750;color:#0B2545;margin:0 0 1rem;letter-spacing:-.01em;}
.skill-legend-item{display:flex;align-items:flex-start;gap:.65rem;margin:.78rem 0;color:#26364B;font-size:.88rem;line-height:1.35;}
.skill-legend-swatch{width:15px;height:15px;min-width:15px;border-radius:3px;margin-top:1px;}
@media (max-width:900px){.skill-legend-card{position:static;margin-top:1rem;}.skill-legend-item{font-size:.84rem;}}
.chip{display:inline-block;background:#F1F5F9;border:1px solid #E2E8F0;color:#334155;padding:.28rem .7rem;border-radius:999px;font-size:.8rem;font-weight:500;margin:0 .4rem .45rem 0;}
.chip-t{display:inline-block;background:#F0FDFA;border:1px solid #99F6E4;color:#115E59;padding:.28rem .7rem;border-radius:999px;font-size:.8rem;font-weight:600;margin:0 .4rem .45rem 0;}
@media (max-width:900px){.grid3{grid-template-columns:1fr !important;}.profile-card{min-height:0;}}
ul.ticks{list-style:none;padding:0;margin:0;}
ul.ticks li{position:relative;padding-left:1.5rem;margin:.45rem 0;color:#334155;font-size:.92rem;line-height:1.5;}
ul.ticks li:before{content:"";position:absolute;left:0;top:.42rem;width:.55rem;height:.55rem;border-radius:50%;background:#14B8A6;box-shadow:0 0 0 3px #CCFBF1;}
ul.checks li:before{content:"✓";background:none;box-shadow:none;color:#0F766E;font-weight:800;top:0;width:auto;height:auto;}
.problem{background:#FFF8F1;border:1px solid #FDE3C8;border-left:5px solid #DD6B20;border-radius:12px;padding:1rem 1.2rem;color:#7B341E;font-size:1rem;}
.problem b{color:#9C4221;}
.why{background:linear-gradient(160deg,#F0FDFA,#fff);border:1px solid #99F6E4;}
.proj-head{display:flex;align-items:center;gap:.9rem;margin:1.2rem 0 1rem;}
.num{flex:none;width:2.6rem;height:2.6rem;border-radius:12px;background:#0B2545;color:#fff;display:grid;place-items:center;font-weight:800;font-size:1.1rem;}
.proj-title{font-size:1.4rem;font-weight:700;color:#0B2545;letter-spacing:-.01em;}
.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;}
.cap .t{font-weight:700;color:#0B2545;font-size:1rem;margin-bottom:.4rem;}
.cap .d{color:#475569;font-size:.9rem;line-height:1.5;min-height:3.2rem;}
.cap .val{margin-top:.8rem;padding-top:.7rem;border-top:1px dashed #E2E8F0;color:#0F766E;font-weight:600;font-size:.85rem;}
.pr{background:#0B2545;color:#E2E8F0;border-radius:14px;padding:1.2rem 1.3rem;}
.pr .t{color:#5EEAD4;font-weight:700;font-size:1.05rem;margin-bottom:.3rem;}
.pr .d{font-size:.9rem;line-height:1.5;}
.fit{display:grid;grid-template-columns:1.1fr 2fr;gap:1rem;align-items:center;padding:.75rem 0;border-bottom:1px solid #EEF2F6;}
.fit:last-child{border-bottom:none;}
.fit .r{font-weight:600;color:#0B2545;}
.fit .e{color:#64748B;font-size:.88rem;}
.dots{display:flex;gap:.3rem;}
.dots i{width:1.35rem;height:.55rem;border-radius:999px;background:#E2E8F0;display:block;}
.dots i.on{background:linear-gradient(90deg,#0F766E,#14B8A6);}
.phase{background:#fff;border:1px solid #E2E8F0;border-radius:14px;overflow:hidden;height:100%;}
.phase .ph{padding:1rem 1.3rem;color:#fff;}
.phase .ph .n{font-size:.72rem;text-transform:uppercase;letter-spacing:.14em;opacity:.8;font-weight:700;}
.phase .ph .h{font-size:1.15rem;font-weight:700;margin-top:.15rem;}
.phase .pb{padding:.6rem 1.3rem 1.1rem;}
.foot{margin-top:3rem;text-align:center;color:#94A3B8;font-size:.82rem;}
.stTabs [role="tablist"]{gap:.35rem;flex-wrap:wrap;background:#fff;border:1px solid #E2E8F0;padding:.4rem;border-radius:14px;box-shadow:0 1px 2px rgba(15,23,42,.04);margin-bottom:.4rem;}
.stTabs [role="tablist"]:before,.stTabs [role="tablist"]:after{display:none;}
.stTabs [data-testid="stTab"]{height:auto;padding:.5rem 1rem;border-radius:10px;background:transparent;border:none;cursor:pointer;}
.stTabs [data-testid="stTab"] p{font-weight:600;color:#475569;font-size:.9rem;}
.stTabs [data-testid="stTab"]:hover{background:#F1F5F9;}
.stTabs [data-testid="stTab"][aria-selected="true"]{background:#0B2545;}
.stTabs [data-testid="stTab"][aria-selected="true"] p{color:#fff;}
.stTabs .react-aria-SelectionIndicator{display:none;}
[class*="st-key-card"]{background:#fff;border:1px solid #E2E8F0;border-radius:14px;padding:1.2rem 1.4rem;box-shadow:0 1px 2px rgba(15,23,42,.04);}
[data-testid="stMetric"]{background:#fff;border:1px solid #E2E8F0;border-radius:12px;padding:.9rem 1rem;}
[data-testid="stMetricValue"]{color:#0B2545;font-weight:700;}

/* Presentation polish */
.hero{padding:2.8rem 3rem 3.8rem;}
.hero-name{font-size:3.15rem;}
.sec{margin-top:3rem;}
.card{transition:transform .18s ease,box-shadow .18s ease;}
.card:hover{transform:translateY(-2px);box-shadow:0 12px 28px -18px rgba(15,23,42,.28);}
.stButton>button,[data-testid="stDownloadButton"] button{border-radius:10px;font-weight:650;}
.stButton>button[kind="primary"]{background:#0B2545;border:1px solid #0B2545;}
.stButton>button[kind="primary"]:hover{background:#13315C;border-color:#13315C;}
[data-testid="stAlert"]{border-radius:12px;}
@media (max-width:700px){
  [data-testid="stMainBlockContainer"]{padding-left:1rem;padding-right:1rem;}
  .hero{padding:1.8rem 1.4rem 2.2rem;}
  .hero-name{font-size:2.25rem;}
  .hero-role{font-size:1rem;}
  .proj-title{font-size:1.15rem;}
}
</style>""")

# ---------------------------------------------------------------- Hero + KPIs
html("""<div class="hero">
<div class="eyebrow">INTERVIEW PORTFOLIO · DATA ENGINEERING, REPORTING & AI</div>
<div class="hero-name">Juhi Ajmera</div>
<div class="hero-role">Technical Lead — Data Engineering &amp; Reporting</div>
<div class="hero-tags"><span>Montreal, QC</span><span>10+ years</span><span>Snowflake · Spark · SQL · Python</span><span>Power BI</span><span>Azure · Airflow · CI/CD</span><span>LLM · GitHub Copilot</span></div>
</div>
<div class="kpis">
<div class="kpi"><div class="v">10+<small>years</small></div><div class="l">Software &amp; data engineering, integration and analytics</div></div>
<div class="kpi"><div class="v">86%<small>faster</small></div><div class="l">Install time cut from 7 h to 1 h</div></div>
<div class="kpi"><div class="v">90<small>days</small></div><div class="l">Historical telemetry ingested &amp; validated</div></div>
<div class="kpi"><div class="v">2<small>patents</small></div><div class="l">Patents</div></div>
<div class="kpi"><div class="v">AI<small>in delivery</small></div><div class="l">LLM + GitHub Copilot</div></div>
</div>""")

# ---------------------------------------------------------------- Summary + career
section("Profile", "Professional summary")
s1, s2 = st.columns([1.08, 1], gap="large")
with s1:
    html("""<div class="card profile-card profile-summary">
      <div class="kicker">Professional profile</div>
      <div class="summary-lead">10+ years turning complex data into reliable business insights.</div>
      <div class="summary-copy">Building data pipelines, integrations, analytics and reporting solutions, with a focus on quality, automation and applied AI.</div>
    </div>""")
with s2:
    html("""<div class="card profile-card profile-cert">
      <h4>Certifications</h4>
      <div class="cert-grid">
        <span>Azure Solutions Architect Expert</span>
        <span>Azure DevOps Engineer Expert</span>
        <span>Azure Data Scientist Associate</span>
        <span>CSM</span><span>CSPO</span><span>SAFe 6</span>
      </div>
    </div>""")


# ---------------------------------------------------------------- Architecture diagrams
# Use the approved visual PNG diagrams stored beside this script.
BASE_DIR = Path(__file__).resolve().parent
DIAGRAM_DIR = BASE_DIR / "juhi_architecture_diagrams"

DIAGRAM_IMAGES = {
    "1": "01-snowflake-ai-reporting.png",
    "2": "02-insurance-claims-reporting.png",
    "3": "03-predictive-maintenance.png",
    "4": "04-deployment-ai-testing.png",
}

projects = {
 "1 · Snowflake + Power BI + AI Reporting": dict(
   short="Snowflake + AI Reporting",
   problem="Support, SLA and feedback data sat in separate systems with unreliable quality.",
   achieved=["ETL/ELT into Snowflake (raw → cleaned → analytics layers)",
             "Python data-quality checks: duplicates, missing values, timestamps, business rules",
             "Power BI dashboards for KPIs, SLA compliance and data quality",
             "LLM assistant using read-only SQL + RAG, answers with source references",
             "Evaluation of SQL correctness, retrieval relevance and factual grounding"],
   stack=["Snowflake", "SQL", "Python", "Power BI", "RAG / Vector search", "Git CI/CD"],
   jd="Consistent, controlled, auditable outputs · Power BI KPIs for data quality & SLA · AI-assisted engineering",
   diagram=True),
 "2 · Insurance Claims Data & Reporting (Financial Services)": dict(
   short="Claims Reporting",
   problem="Claims data had gaps, duplicates and inconsistencies, so reports could not be trusted.",
   achieved=["Python + SQL proof of concept to extract, transform and organise claims data",
             "Data-quality and validation rules for consistent reporting datasets",
             "Structured stakeholder reports",
             "Documented logic and validation rules for traceability"],
   stack=["Python", "SQL", "Validation rules", "Reporting"],
   jd="Finance domain · Controlled, traceable reporting · Requirements to delivery with stakeholders",
   diagram=True),
 "3 · Predictive Maintenance Data Integration": dict(
   short="Predictive Maintenance",
   problem="Industrial equipment telemetry could not reach prediction algorithms reliably.",
   achieved=["Ingestion pipelines via Kepware + MQTT into Azure Blob Storage",
             "Up to 90 days of historical data made accessible and validated",
             "Apache Spark processing, Snowflake storage and analytics",
             "Adapters integrating vibration-prediction algorithms with the platform"],
   stack=["Apache Spark", "Snowflake", "Azure", "MQTT", "Python", "Airflow"],
   jd="Telemetry integration · Spark processing · Predictive-maintenance algorithm integration",
   diagram=True),
 "4 · Automated Deployment & AI-Assisted Testing": dict(
   short="DevOps & AI Testing",
   problem="Manual, inconsistent installs took 7 hours; regressions were caught late.",
   achieved=["Python framework automating setup, DB config, certificates and services",
             "Install time cut from 7h to 1h (~86%)",
             "GitHub Copilot + coding agent for Molecule test automation",
             "Automated tests wired into GitHub CI/CD"],
   stack=["Python", "Ansible", "Molecule", "GitHub Actions", "GitHub Copilot"],
   jd="Platform hygiene & DevOps remediation · CI/CD, environment controls · AI-assisted dev tools",
   diagram=True),
}

section("Portfolio", "Selected work", "Project architecture diagrams and concise role alignment.")
tabs = st.tabs([p["short"] for p in projects.values()] + ["JD Fit"])

for tab, (name, p) in zip(tabs, projects.items()):
    num, title = name.split(" · ", 1)
    with tab:
        html(f'<div class="proj-head"><div class="num">{num}</div><div class="proj-title">{title}</div></div>'
             f'<div class="problem"><b>Challenge:</b> {p["problem"]}</div>')
        with st.container(key=f"card_arch_{num}"):
            html('<div class="kicker">Solution architecture</div>')
            diagram_path = DIAGRAM_DIR / DIAGRAM_IMAGES[num]
            if diagram_path.exists():
                st.image(str(diagram_path), use_container_width=True)
            else:
                st.error(
                    f"Architecture image not found: {diagram_path.name}. "
                    "Keep the juhi_architecture_diagrams folder beside this Python file."
                )
        with st.expander("Key contributions", expanded=False):
            st.markdown(" · ".join(p["achieved"]))
        if num == "2":
            st.caption("Proof of concept, not a production financial-services platform.")
        else:
            st.caption("Simplified architecture view of the workflow and components described for this project.")
        if num == "4":
            st.write("")
            with st.container(key="card_install"):
                fig = go.Figure(go.Bar(x=[7, 1], y=["Before", "After"], orientation="h", text=["7 hours", "1 hour"],
                                       textposition="outside", marker_color=["#CBD5E1", TEAL], width=0.55))
                fig.update_layout(title="Installation time — 86% faster", xaxis_title="Hours", xaxis_range=[0, 8.2])
                fig.update_yaxes(autorange="reversed", gridcolor="rgba(0,0,0,0)")
                st.plotly_chart(style_fig(fig, 240), width="stretch", config={"displayModeBar": False})

with tabs[4]:
    section("JD fit", "Role alignment",
            "One view of the tools and skills listed in your resume, with suggested self-ratings.")

    # Single chart covering resume tools and technologies. Axiom and Scala are
    # retained at 1/5 because the user specifically requested those ratings.
    skill_ratings = [
        ("SQL", 4, "Data engineering"),
        ("Python", 3, "Data engineering"),
        ("Snowflake", 4, "Data engineering"),
        ("Apache Spark", 3, "Data engineering"),
        ("SQL Server", 4, "Data engineering"),
        ("PostgreSQL", 3, "Data engineering"),
        ("ETL / ELT", 4, "Data engineering"),
        ("Data pipelines", 4, "Data engineering"),
        ("Data modeling", 3, "Data engineering"),
        ("Data quality & validation", 4, "Data engineering"),
        ("Microsoft Azure", 4, "Cloud & integration"),
        ("Azure Blob Storage", 3, "Cloud & integration"),
        ("Azure VMs", 3, "Cloud & integration"),
        ("Azure SDK", 3, "Cloud & integration"),
        ("MQTT", 3, "Cloud & integration"),
        ("Kepware", 3, "Cloud & integration"),
        ("ThingWorx", 3, "Cloud & integration"),
        ("APIs", 3, "Cloud & integration"),
        ("Apache Airflow", 3, "Cloud & orchestration"),
        ("Power BI", 4, "Reporting & analytics"),
        ("KPI / SLA reporting", 4, "Reporting & analytics"),
        ("Git", 4, "DevOps & testing"),
        ("GitHub", 4, "DevOps & testing"),
        ("GitHub Actions", 3, "DevOps & testing"),
        ("CI/CD", 3, "DevOps & testing"),
        ("Docker", 3, "DevOps & testing"),
        ("Kubernetes", 3, "DevOps & testing"),
        ("Ansible", 3, "DevOps & testing"),
        ("Molecule", 3, "DevOps & testing"),
        ("Coverity", 2, "DevOps & testing"),
        ("Black Duck", 2, "DevOps & testing"),
        ("Jira", 4, "Delivery & collaboration"),
        ("Confluence", 4, "Delivery & collaboration"),
        ("LLM integration", 3, "AI engineering"),
        ("RAG / vector search", 3, "AI engineering"),
        ("GitHub Copilot", 4, "AI engineering"),
        ("AI evaluation", 3, "AI engineering"),
        ("Axiom", 1, "JD technologies · limited familiarity"),
        ("Scala", 1, "JD technologies · limited familiarity"),
    ]
    chart_df = pd.DataFrame(skill_ratings, columns=["Skill / tool", "Rating", "Area"])
    area_order = [
        "AI engineering", "Cloud & integration", "Cloud & orchestration",
        "Data engineering", "Delivery & collaboration", "DevOps & testing",
        "JD technologies · limited familiarity", "Reporting & analytics",
    ]
    area_colors = {
        "AI engineering": "#0875D1",
        "Cloud & integration": "#75C4F5",
        "Cloud & orchestration": "#F04444",
        "Data engineering": "#F5A0A0",
        "Delivery & collaboration": "#22B8A5",
        "DevOps & testing": "#69E99A",
        "JD technologies · limited familiarity": "#FF8A00",
        "Reporting & analytics": "#FFD166",
    }
    area_rank = {name: index for index, name in enumerate(area_order)}
    sorted_df = chart_df.assign(_area_order=chart_df["Area"].map(area_rank)).sort_values(
        ["_area_order", "Rating", "Skill / tool"], ascending=[True, True, True]
    ).drop(columns="_area_order")

    # Chart on the left, category key in a separate card on the right.
    chart_col, legend_col = st.columns([3.7, 1.35], gap="large")
    chart_height = max(760, 28 * len(sorted_df) + 100)
    with chart_col:
        fig = px.bar(
            sorted_df, x="Rating", y="Skill / tool", color="Area", orientation="h",
            text=sorted_df["Rating"].map(lambda value: f"{value}/5"),
            hover_data={"Area": True, "Rating": True, "Skill / tool": True},
            category_orders={
                "Skill / tool": sorted_df["Skill / tool"].tolist(),
                "Area": area_order,
            },
            color_discrete_map=area_colors,
        )
        fig.update_layout(
            title=None,
            xaxis=dict(range=[0, 5.6], tickvals=[1, 2, 3, 4, 5], title="Rating out of 5"),
            yaxis=dict(title=None, autorange="reversed", tickfont=dict(size=11)),
            height=chart_height, showlegend=False,
            margin=dict(l=8, r=42, t=12, b=38), bargap=0.28,
        )
        fig.update_traces(textposition="outside", cliponaxis=False, marker_line_width=0)
        st.plotly_chart(
            style_fig(fig, chart_height), width="stretch",
            config={"displayModeBar": False},
        )

    with legend_col:
        legend_items = "".join(
            f'<div class="skill-legend-item"><span class="skill-legend-swatch" style="background:{area_colors[area]}"></span><span>{area}</span></div>'
            for area in area_order
        )
        html(f"""
        <div class="skill-legend-card">
          <div class="skill-legend-title">Skill Categories</div>
          {legend_items}
        </div>
        """)



html('<div class="foot">Juhi Ajmera · Built in Python + Streamlit</div>')
