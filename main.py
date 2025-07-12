import streamlit as st
import pandas as pd

atp_rankings_current = pd.read_csv("data/atp_rankings_current.csv", index_col="player")
atp_ranking_20s = pd.read_csv("data/atp_rankings_20s.csv", index_col="player")
atp_ranking_10s = pd.read_csv("data/atp_rankings_10s.csv", index_col="player")
atp_players = pd.read_csv("data/atp_players.csv", index_col="player_id")

ranks = (
    pd.concat([atp_rankings_current, atp_ranking_20s, atp_ranking_10s])
    .join(atp_players, how="left")
)

ranks["ranking_date"] = pd.to_datetime(ranks["ranking_date"], format="%Y%m%d")
ranks["name"] = ranks["name_first"].fillna("") + " " + ranks["name_last"].fillna("")
ranks = ranks[["ranking_date", "name", "points", "rank"]]

names = list(set(ranks["name"].tolist()))
chosen = st.sidebar.multiselect("Points Chart", names, default=["Carlos Alcaraz", "Jannik Sinner"])
show = ranks[ranks["name"].isin(chosen)]

st.title("ATP Points")
st.line_chart(show, x="ranking_date", y="points", color="name")
