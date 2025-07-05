import streamlit as st
from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI
from langchain.agents.agent_types import AgentType

# Fonction simulée pour répondre à des questions réglementaires
def urssaf_info(question: str) -> str:
    faq = {
        "assiette sociale": "Depuis 2025, l'assiette sociale est simplifiée : elle correspond au revenu brut diminué d’un abattement de 26 %, sans déduction des cotisations sociales.",
        "cotisation retraite": "La part de la cotisation retraite augmente pour améliorer les droits des indépendants.",
        "attestation de vigilance": "Elle est obligatoire pour tout contrat supérieur à 5 000 € HT, à fournir tous les 6 mois.",
        "acre": "L'ACRE permet une exonération partielle de début d'activité pour les auto-entrepreneurs.",
        "déclaration": "Les auto-entrepreneurs doivent déclarer leur chiffre d'affaires mensuellement ou trimestriellement sur autoentrepreneur.urssaf.fr.",
        "arnaque": "Attention aux faux courriers et aux arnaques : l'Urssaf ne demande jamais de paiement par email ou SMS."
    }
    for mot_clé, réponse in faq.items():
        if mot_clé in question.lower():
            return réponse
    return "Je vous recommande de consulter le site officiel de l'Urssaf ou de contacter un conseiller pour cette question spécifique."

# Définir l'outil
outil_urssaf = Tool(
    name="InfoUrssaf",
    func=urssaf_info,
    description="Répond aux questions sur les règles Urssaf pour les auto-entrepreneurs et indépendants."
)

# Initialiser le modèle
llm = OpenAI(temperature=0)

# Créer l’agent
agent = initialize_agent(
    tools=[outil_urssaf],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False
)

# Interface Streamlit
st.set_page_config(page_title="Agent IA Urssaf", page_icon="📄")
st.title("🤖 Agent IA Urssaf")
st.write("Posez une question sur les règles Urssaf pour les auto-entrepreneurs et travailleurs indépendants.")

question = st.text_input("Votre question :")

if question:
    with st.spinner("L'agent réfléchit..."):
        reponse = agent.run(question)
        st.success(reponse)
