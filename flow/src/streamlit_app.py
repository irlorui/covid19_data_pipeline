import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from db_utils import Database

## Create DB connection
db = Database(
    dbname="clinical_trials",
    user="admin",
    password="admin",
    host="localhost",
    port=5432
)
conn = db.get_connection()

st.set_page_config(page_title="Clinical Trials Dashboard", layout="wide")

st.title("🧪 Clinical Trials Dashboard")

# ---- Load data from prod schema ----
@st.cache_data
def load_data():
    trial = pd.read_sql("SELECT * FROM prod.trial", conn)
    study_type = pd.read_sql("SELECT * FROM prod.study_type", conn)
    phase = pd.read_sql("SELECT * FROM prod.phase", conn)
    condition = pd.read_sql("SELECT * FROM prod.condition", conn)
    intervention = pd.read_sql("SELECT * FROM prod.intervention", conn)
    trial_condition = pd.read_sql("SELECT * FROM prod.trial_condition", conn)
    trial_intervention = pd.read_sql("SELECT * FROM prod.trial_intervention", conn)
    trial_country = pd.read_sql("SELECT * FROM prod.trial_country", conn)
    country = pd.read_sql("SELECT * FROM prod.country", conn)
    return trial, study_type, phase, condition, intervention, trial_condition, trial_intervention, trial_country, country

trial, study_type, phase, condition, intervention, trial_condition, trial_intervention, trial_country, country = load_data()

# Join trials with FK values
trial_full = trial.merge(study_type, on="study_type_id", how="left") \
                  .merge(phase, on="phase_id", how="left")

# ------------------------------------------------------------------------------------------
# 1 - Total Trials && Filtered by study type or Phase
# ------------------------------------------------------------------------------------------

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Total Clinical Trials")
    total_trials = trial['trial_id'].nunique()
    st.metric(label="", value=f"{total_trials:,}")

# =======================
# FILTERS
# =======================
with col2:
    st.markdown("### Filter Trials")
    selected_study_type = st.selectbox("Study Type",
                                       options=["All"] + sorted(trial_full["study_type_name"].dropna().unique().tolist()))
    selected_phase = st.selectbox("Phase",
                                  options=["All"] + sorted(trial_full["phase_name"].dropna().unique().tolist()))


# =======================
# Apply Filters
# =======================
filtered_df = trial_full.copy()

if selected_study_type != "All":
    filtered_df = filtered_df[filtered_df["study_type_name"] == selected_study_type]

if selected_phase != "All":
    filtered_df = filtered_df[filtered_df["phase_name"] == selected_phase]

# =======================
# DISPLAY RESULTING GRAPH
# =======================
st.markdown("### Filtered Trials by Study Type & Phase")

grouped = filtered_df.groupby(['study_type_name', 'phase_name']).size().reset_index(name="count")

if grouped.empty:
    st.warning("No data found for selected filters.")
else:
    fig, ax = plt.subplots()
    sns.barplot(data=grouped, x="count", y="study_type_name", hue="phase_name", ax=ax)
    ax.set_title("Filtered Trials Distribution")
    ax.set_xlabel("Number of Trials")
    ax.set_ylabel("Study Type")
    fig.tight_layout()
    st.pyplot(fig)



# ------------------------------------------------------------------------------------------
# 2. Most Common Conditions & Geographic Distribution
# ------------------------------------------------------------------------------------------

col1, col2 = st.columns(2)

with col1:    
    st.markdown("### Most Common Conditions Being Studied")
    trial_condition_full = trial_condition.merge(condition, on="condition_id", how="left")
    top_conditions = trial_condition_full['condition_name'].value_counts().head(10)

    fig, ax = plt.subplots()
    sns.barplot(x=top_conditions.index, y=top_conditions.values, ax=ax)
    ax.set_title("Top 10 Conditions")
    ax.set_xlabel("Condition")
    ax.set_ylabel("Trial Count")
    ax.set_xticks(range(len(top_conditions.index)))
    ax.set_xticklabels(top_conditions.index, rotation=30, ha='right')
    fig.tight_layout()
    st.pyplot(fig)

with col2:
    st.markdown("### Geographic Distribution")
    trial_country_full = trial_country.merge(country, on="country_id")
    geo_dist = trial_country_full['country_name'].value_counts().head(10)

    fig, ax = plt.subplots()
    sns.barplot(x=geo_dist.index, y=geo_dist.values, ax=ax)
    ax.set_title("Top 10 Countries with Most Trials")
    ax.set_xlabel("Country")
    ax.set_ylabel("Trial Count")
    ax.set_xticks(range(len(geo_dist.index)))
    ax.set_xticklabels(geo_dist.index, rotation=30, ha='right')
    fig.tight_layout()
    st.pyplot(fig)


# ------------------------------------------------------------------------------------------
# 3. Interventions with Highest Completion Rate && Timeline Analysis of Study Durations
# ------------------------------------------------------------------------------------------

col1, col2 = st.columns(2)

with col1:    
    st.markdown("### Interventions with Highest Completion Rate")
    completed_trials = trial[trial['completed_at'].notnull()]
    completed_with_interv = completed_trials.merge(trial_intervention, on="trial_id").merge(intervention, on="intervention_id")
    completion_rate = completed_with_interv['intervention_name'].value_counts().head(10)

    fig, ax = plt.subplots()
    sns.barplot(x=completion_rate.index, y=completion_rate.values, ax=ax)
    ax.set_title("Top 10 Interventions with most Completed Trials")
    ax.set_xlabel("Intervention")
    ax.set_xticks(range(len(completion_rate.index)))
    ax.set_xticklabels(completion_rate.index, rotation=30, ha='right')
    st.pyplot(fig)

with col2:
    st.markdown("### Timeline Analysis")
    trial_duration = trial.copy()
    trial_duration = trial_duration[trial_duration['started_at'].notnull() & trial_duration['completed_at'].notnull()]
    trial_duration['duration_days'] = (pd.to_datetime(trial_duration['completed_at']) - pd.to_datetime(trial_duration['started_at'])).dt.days

    fig, ax = plt.subplots()
    sns.histplot(trial_duration['duration_days'], bins=30, ax=ax)
    ax.set_title("Trial Durations Histogram")
    ax.set_xlabel("Days")
    ax.set_ylabel("Trial Count")
    fig.tight_layout()
    st.pyplot(fig)

st.success("✅ Dashboard rendered successfully.")

conn.close()
