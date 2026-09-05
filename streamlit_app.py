import streamlit as st
import random
import time
import datetime
import json

# Configuration de la page
st.set_page_config(
    page_title="L'Éveil en Classe - Jeu Interactif Bilingue",
    page_icon="🎴",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Style CSS personnalisé pour l'ambiance chaleureuse de la classe et le support de l'hébreu
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&family=Quicksand:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Quicksand', sans-serif;
    }
    
    .main-title {
        font-family: 'Fredoka One', cursive;
        color: #4A90E2;
        text-align: center;
        font-size: 2.8rem;
        margin-bottom: 5px;
        text-shadow: 2px 2px #E6F0FA;
    }
    
    .subtitle {
        text-align: center;
        color: #7F8C8D;
        font-size: 1.2rem;
        margin-bottom: 30px;
    }
    
    /* Style de la carte virtuelle */
    .card-container {
        background-color: #FFFFFF;
        border-radius: 25px;
        padding: 35px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.08);
        text-align: center;
        margin: 20px auto;
        max-width: 500px;
        transition: transform 0.3s ease;
    }
    
    .card-container:hover {
        transform: translateY(-5px);
    }
    
    .card-header-badge {
        font-size: 0.9rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 2px;
        padding: 6px 15px;
        border-radius: 50px;
        display: inline-block;
        margin-bottom: 20px;
    }
    
    .card-text {
        font-family: 'Quicksand', sans-serif;
        font-weight: 700;
        font-size: 1.6rem;
        line-height: 1.5;
        color: #2C3E50;
        margin: 20px 0 10px 0;
        font-style: italic;
    }

    .card-text-hebrew {
        font-family: 'Quicksand', 'Segoe UI', Arial, sans-serif;
        font-weight: 700;
        font-size: 1.8rem;
        line-height: 1.5;
        color: #34495E;
        margin: 10px 0 20px 0;
        direction: rtl;
        text-align: center;
    }
    
    .card-footer-info {
        font-size: 0.85rem;
        color: #BDC3C7;
        margin-top: 15px;
        border-top: 1px dashed #ECF0F1;
        padding-top: 15px;
    }
    
    /* Zone de défi */
    .challenge-box {
        background-color: #F9EBEA;
        border-left: 5px solid #E74C3C;
        border-radius: 8px;
        padding: 15px;
        margin: 20px 0;
        font-size: 1.1rem;
    }
    
    /* Badges */
    .badge-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
        gap: 15px;
        margin-top: 20px;
    }
    
    .badge-card {
        background-color: #F8F9F9;
        border: 2px solid #E5E8E8;
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .badge-active {
        background-color: #E8F8F5;
        border: 2px solid #2ECC71;
        box-shadow: 0 5px 15px rgba(46, 204, 113, 0.15);
    }
    
    .badge-icon {
        font-size: 2.2rem;
        margin-bottom: 8px;
    }
    
    .badge-title {
        font-weight: 700;
        font-size: 0.9rem;
        color: #34495E;
    }
</style>
""", unsafe_allow_html=True)

# Définition des données du jeu (les 12 thèmes, couleurs, icônes, badges et les 60 cartes)
THEMES_INFO = {
    "Effort & persévérance": {
        "color": "#E67E22", "bg_light": "#FDF2E9", "icon": "⛰️", 
        "badge_name": "Sommet d'Or", "badge_desc": "Pour ta constance et tes efforts continus."
    },
    "Erreur & apprentissage": {
        "color": "#F1C40F", "bg_light": "#FEF9E7", "icon": "💡", 
        "badge_name": "L'Étincelle", "badge_desc": "Pour avoir transformé une erreur en leçon."
    },
    "Coopération & entraide": {
        "color": "#1ABC9C", "bg_light": "#E8F8F5", "icon": "🤝", 
        "badge_name": "L'Alliance", "badge_desc": "Pour avoir additionné tes forces en groupe."
    },
    "Inclusion & diversité": {
        "color": "#9B59B6", "bg_light": "#F5EEF8", "icon": "🌈", 
        "badge_name": "Arc-en-Ciel", "badge_desc": "Pour avoir célébré la richesse du groupe."
    },
    "Bienveillance & gentillesse": {
        "color": "#FF6B81", "bg_light": "#FFEFF1", "icon": "❤️", 
        "badge_name": "Grand Cœur", "badge_desc": "Pour avoir offert de la douceur ou un sourire."
    },
    "Confiance en soi": {
        "color": "#F39C12", "bg_light": "#FEF5E7", "icon": "⭐", 
        "badge_name": "Étoile Intérieure", "badge_desc": "Pour être fier(e) de toi sans chercher la perfection."
    },
    "Curiosité & apprentissage": {
        "color": "#3498DB", "bg_light": "#EBF5FB", "icon": "🔍", 
        "badge_name": "Explorateur", "badge_desc": "Pour avoir posé des questions et cherché à savoir."
    },
    "Courage & audace": {
        "color": "#E74C3C", "bg_light": "#FDEDEC", "icon": "⚡", 
        "badge_name": "Lion Courageux", "badge_desc": "Pour avoir osé sortir de ta zone de confort."
    },
    "Gratitude & positivité": {
        "color": "#FF9F43", "bg_light": "#FFF3E6", "icon": "☀️", 
        "badge_name": "Rayon de Soleil", "badge_desc": "Pour avoir remarqué les belles choses de ton jour."
    },
    "Respect & écoute": {
        "color": "#2ECC71", "bg_light": "#EAF2F8", "icon": "💬", 
        "badge_name": "Havre de Paix", "badge_desc": "Pour ton écoute attentive et respectueuse."
    },
    "Créativité & imagination": {
        "color": "#8E44AD", "bg_light": "#F4ECF7", "icon": "🎨", 
        "badge_name": "Créateur d'Univers", "badge_desc": "Pour avoir osé une idée inattendue et originale."
    },
    "Responsabilité & engagement": {
        "color": "#27AE60", "bg_light": "#E8F8F5", "icon": "🌱", 
        "badge_name": "Jeune Pousse", "badge_desc": "Pour avoir choisi de faire ta part activement."
    }
}

# Les 60 cartes du deck avec les citations bilingues français / hébreu
CARDS_DATA = [
    # Effort & persévérance (1-5)
    {
        "num": 1, "theme": "Effort & persévérance", 
        "quote": "Ce n'est pas la vitesse qui compte, c'est la constance.", 
        "quote_he": "לא המהירות קובעת, אלא ההתמדה.", 
        "challenge": "Pense à une activité que tu as apprise lentement, mais sûrement. Écris-la ici."
    },
    {
        "num": 2, "theme": "Effort & persévérance", 
        "quote": "Un effort répété vaut mieux qu'un talent qui abandonne.", 
        "quote_he": "מאמץ מתמשך שווה יותר מכישרון שמוותר.", 
        "challenge": "Nomme une chose que tu as réussie uniquement en essayant plusieurs fois."
    },
    {
        "num": 3, "theme": "Effort & persévérance", 
        "quote": "Tomber fait partie du chemin, se relever fait la différence.", 
        "quote_he": "ליפול זה חלק מהדרך, לקום זה מה שעושה את ההבדל.", 
        "challenge": "Raconte un moment où tu as eu envie de baisser les bras, mais où tu as choisi de continuer."
    },
    {
        "num": 4, "theme": "Effort & persévérance", 
        "quote": "Le progrès se construit un jour à la fois.", 
        "quote_he": "התקדמות נבנית יום אחד בכל פעם.", 
        "challenge": "Quel petit pas peux-tu faire aujourd'hui pour progresser dans la matière de ton choix ?"
    },
    {
        "num": 5, "theme": "Effort & persévérance", 
        "quote": "Persévérer, c'est continuer à croire en soi quand c'est difficile.", 
        "quote_he": "להתמיד זה להמשיך להאמין בעצמך גם כשקשה.", 
        "challenge": "Écris une phrase d'encouragement que tu pourrais te dire à toi-même lors d'un exercice difficile."
    },
    
    # Erreur & apprentissage (6-10)
    {
        "num": 6, "theme": "Erreur & apprentissage", 
        "quote": "Une erreur bien comprise vaut mille leçons apprises par cœur.", 
        "quote_he": "טעות שמבינים אותה שווה יותר מאלף שיעורים שלמדו בעל פה.", 
        "challenge": "Explique une erreur commise récemment à l'école et ce que tu as compris grâce à elle."
    },
    {
        "num": 7, "theme": "Erreur & apprentissage", 
        "quote": "Se tromper, c'est la preuve que tu essaies vraiment.", 
        "quote_he": "לטעות זו ההוכחה שאתה באמת מנסה.", 
        "challenge": "Célèbre une erreur aujourd'hui ! Écris : 'Aujourd'hui, je me suis trompé(e) sur ... et c'est super car j'ai compris ...'"
    },
    {
        "num": 8, "theme": "Erreur & apprentissage", 
        "quote": "Le cerveau grandit chaque fois qu'il relève un défi.", 
        "quote_he": "המוח גדל בכל פעם שהוא מתמודד עם אתגר.", 
        "challenge": "Quel a été ton plus grand défi intellectuel de la semaine ? Comment ton cerveau a-t-il grandi ?"
    },
    {
        "num": 9, "theme": "Erreur & apprentissage", 
        "quote": "Ce que tu ne sais pas encore, tu peux l'apprendre demain.", 
        "quote_he": "מה שאתה עוד לא יודע, תוכל ללמוד מחר.", 
        "challenge": "Y a-t-il quelque chose qui te paraît difficile aujourd'hui ? Écris : 'Je ne sais pas encore faire ..., mais je vais l'apprendre !'"
    },
    {
        "num": 10, "theme": "Erreur & apprentissage", 
        "quote": "Douter n'est pas un problème, c'est le début de la compréhension.", 
        "quote_he": "לפקפק זה לא בעיה, זו ההתחלה של ההבנה.", 
        "challenge": "Pose par écrit une question sur un sujet qui te fait douter ou t'intrigue."
    },

    # Coopération & entraide (11-15)
    {
        "num": 11, "theme": "Coopération & entraide", 
        "quote": "À plusieurs, une idée devient un projet.", 
        "quote_he": "יחד, רעיון הופך לפרויקט.", 
        "challenge": "Pense à un projet que tu aimerais faire avec tes camarades. Décris-le brièvement."
    },
    {
        "num": 12, "theme": "Coopération & entraide", 
        "quote": "Aider quelqu'un, c'est aussi apprendre de lui.", 
        "quote_he": "לעזור למישהו זה גם ללמוד ממנו.", 
        "challenge": "Raconte un moment où tu as aidé un camarade et où cela t'a fait du bien ou t'a appris quelque chose."
    },
    {
        "num": 13, "theme": "Coopération & entraide", 
        "quote": "Une classe forte est une classe qui s'écoute.", 
        "quote_he": "כיתה חזקה היא כיתה שמקשיבה לעצמה.", 
        "challenge": "Qu'est-ce que bien écouter signifie pour toi ? Écris une action concrète d'écoute pour aujourd'hui."
    },
    {
        "num": 14, "theme": "Coopération & entraide", 
        "quote": "Personne ne réussit vraiment seul.", 
        "quote_he": "אף אחד לא באמת מצליח לבד.", 
        "challenge": "Remercie par écrit un camarade ou un adulte de l'école qui t'a aidé(e) récemment."
    },
    {
        "num": 15, "theme": "Coopération & entraide", 
        "quote": "Travailler ensemble, c'est additionner nos forces.", 
        "quote_he": "לעבוד ביחד זה לחבר את הכוחות שלנו.", 
        "challenge": "Quelle est ta 'super-force' (ex: le dessin, l'organisation, le calcul, le calme) que tu peux partager avec un groupe ?"
    },

    # Inclusion & diversité (16-20)
    {
        "num": 16, "theme": "Inclusion & diversité", 
        "quote": "Nos différences sont ce qui rend le groupe complet.", 
        "quote_he": "ההבדלים בינינו הם מה שהופך את הקבוצה לשלמה.", 
        "challenge": "Trouve un camarade qui a un goût ou une passion différente des tiennes. Écris ce que cela t'apporte de différent."
    },
    {
        "num": 17, "theme": "Inclusion & diversité", 
        "quote": "Il y a plusieurs façons d'être intelligent, et toutes comptent.", 
        "quote_he": "יש כמה דרכים להיות חכם, וכולן חשובות.", 
        "challenge": "Selon toi, quelles sont tes deux formes d'intelligence préférées (manuelle, logique, artistique, sportive, écoute...) ?"
    },
    {
        "num": 18, "theme": "Inclusion & diversité", 
        "quote": "Personne n'est un invité ici, tout le monde est chez soi.", 
        "quote_he": "אף אחד כאן הוא לא אורח, כולם בבית.", 
        "challenge": "Écris un petit geste simple pour que chaque élève se sente bienvenu dans la classe."
    },
    {
        "num": 19, "theme": "Inclusion & diversité", 
        "quote": "Comprendre quelqu'un de différent, c'est agrandir son propre monde.", 
        "quote_he": "להבין מישהו שונה ממך זה להרחיב את העולם שלך.", 
        "challenge": "Raconte une fois où tu as parlé avec quelqu'un d'un milieu ou parcours différent. Qu'as-tu découvert ?"
    },
    {
        "num": 20, "theme": "Inclusion & diversité", 
        "quote": "Une classe riche rassemble mille façons différentes d'être soi.", 
        "quote_he": "כיתה עשירה מאגדת בתוכה אלף דרכים שונות להיות עצמך.", 
        "challenge": "Écris trois mots positifs qui te décrivent uniquement toi, et explique pourquoi c'est une force pour la classe."
    },

    # Bienveillance & gentillesse (21-25)
    {
        "num": 21, "theme": "Bienveillance & gentillesse", 
        "quote": "Un mot gentil ne coûte rien et peut changer une journée.", 
        "quote_he": "מילה טובה לא עולה כלום ויכולה לשנות יום שלם.", 
        "challenge": "Écris un mot gentil destiné à quelqu'un dans la classe. Tu pourras aller lui dire après !"
    },
    {
        "num": 22, "theme": "Bienveillance & gentillesse", 
        "quote": "Être doux avec les autres n'est jamais un signe de faiblesse.", 
        "quote_he": "להיות עדין עם אחרים הוא לעולם לא סימן לחולשה.", 
        "challenge": "Pense à une situation où tu as choisi d'être doux et patient au lieu de t'énerver. Comment t'es-tu senti(e) ?"
    },
    {
        "num": 23, "theme": "Bienveillance & gentillesse", 
        "quote": "Un sourire donné au bon moment peut tout changer.", 
        "quote_he": "חיוך שניתן ברגע הנכון יכול לשנות הכול.", 
        "challenge": "Aujourd'hui, relève le défi de sourire sincèrement à trois personnes différentes. Note ce que tu as ressenti."
    },
    {
        "num": 24, "theme": "Bienveillance & gentillesse", 
        "quote": "La bienveillance commence par une écoute sincère.", 
        "quote_he": "טוב לב מתחיל בהקשבה כנה.", 
        "challenge": "Prends 2 minutes pour écouter un camarade te raconter quelque chose, sans l'interrompre. Écris tes impressions."
    },
    {
        "num": 25, "theme": "Bienveillance & gentillesse", 
        "quote": "Prendre soin des autres, c'est aussi prendre soin de soi.", 
        "quote_he": "לדאוג לאחרים זה גם לדאוג לעצמך.", 
        "challenge": "Comment as-tu pris soin de toi aujourd'hui ? (Une pause tranquille, une bonne lecture, un jeu...)"
    },

    # Confiance en soi (26-30)
    {
        "num": 26, "theme": "Confiance en soi", 
        "quote": "Tu n'as pas besoin d'être parfait pour être fier de toi.", 
        "quote_he": "אתה לא צריך להיות מושלם כדי להיות גאה בעצמך.", 
        "challenge": "Écris une action ou une réussite de ta semaine dont tu es fier(e), même si elle n'était pas parfaitement parfaite."
    },
    {
        "num": 27, "theme": "Confiance en soi", 
        "quote": "Ta valeur ne dépend pas d'une note.", 
        "quote_he": "הערך שלך לא נמדד בציון.", 
        "challenge": "Quelles sont tes qualités humaines importantes (gentillesse, humour, écoute...) qui ne s'écrivent pas sur un bulletin de notes ?"
    },
    {
        "num": 28, "theme": "Confiance en soi", 
        "quote": "Crois en toi, même les jours où c'est difficile.", 
        "quote_he": "תאמין בעצמך, גם בימים הקשים.", 
        "challenge": "Visualise un bouclier imaginaire. Écris 3 forces intérieures ou qualités que tu inscrirais dessus pour te protéger du doute."
    },
    {
        "num": 29, "theme": "Confiance en soi", 
        "quote": "Ce que tu penses de toi compte plus que ce que les autres en disent.", 
        "quote_he": "מה שאתה חושב על עצמך חשוב יותר ממה שאחרים אומרים.", 
        "challenge": "Écris un compliment sincère que tu te fais à toi-même aujourd'hui."
    },
    {
        "num": 30, "theme": "Confiance en soi", 
        "quote": "Tu as le droit de te tromper et de continuer à avancer.", 
        "quote_he": "מותר לך לטעות ולהמשיך להתקדם.", 
        "challenge": "Complète cette phrase : 'Si j'étais certain(e) de ne pas échouer, la première chose que j'essaierais de faire serait de...'"
    },

    # Curiosité & apprentissage (31-35)
    {
        "num": 31, "theme": "Curiosité & apprentissage", 
        "quote": "Une question ouvre toujours plus de portes qu'elle n'en ferme.", 
        "quote_he": "שאלה תמיד פותחת יותר דלתות משהיא סוגרת.", 
        "challenge": "Écris une grande question sur la vie, la nature, la science ou l'histoire à laquelle tu aimerais trouver une réponse."
    },
    {
        "num": 32, "theme": "Curiosité & apprentissage", 
        "quote": "La curiosité est le premier pas vers la découverte.", 
        "quote_he": "סקרנות היא הצעד הראשון לגילוי.", 
        "challenge": "Quel sujet ou quel livre a attisé ta curiosité cette semaine ? Pourquoi ?"
    },
    {
        "num": 33, "theme": "Curiosité & apprentissage", 
        "quote": "Apprendre, c'est accepter de ne pas tout savoir.", 
        "quote_he": "ללמוד זה להסכים לא לדעת הכול.", 
        "challenge": "Écris pourquoi, selon toi, il est courageux et utile de dire 'Je ne sais pas, mais je vais chercher !'"
    },
    {
        "num": 34, "theme": "Curiosité & apprentissage", 
        "quote": "Chaque livre, chaque question, chaque essai t'emmène plus loin.", 
        "quote_he": "כל ספר, כל שאלה, כל ניסיון לוקחים אותך רחוק יותר.", 
        "challenge": "Nomme un domaine, une culture ou un sport que tu ne connais pas du tout mais que tu serais curieux(se) de découvrir."
    },
    {
        "num": 35, "theme": "Curiosité & apprentissage", 
        "quote": "Le savoir se construit petit à petit, comme une maison.", 
        "quote_he": "הידע נבנה לאט לאט, כמו בית.", 
        "challenge": "Quelle petite idée ou information nouvelle as-tu apprise aujourd'hui à l'école ou ailleurs ?"
    },

    # Courage & audace (36-40)
    {
        "num": 36, "theme": "Courage & audace", 
        "quote": "Le courage, ce n'est pas l'absence de peur, c'est avancer malgré elle.", 
        "quote_he": "אומץ הוא לא היעדר פחד, אלא להתקדם למרותו.", 
        "challenge": "Raconte un moment de ta vie où tu as eu peur, mais où tu as choisi d'agir quand même."
    },
    {
        "num": 37, "theme": "Courage & audace", 
        "quote": "Lever la main quand on n'est pas sûr, c'est déjà un acte de courage.", 
        "quote_he": "להרים יד כשלא בטוחים זו כבר פעולה אמיצה.", 
        "challenge": "Aujourd'hui, tente de lever la main en classe pour poser une question ou donner une réponse, même avec un doute ! Décris ton ressenti."
    },
    {
        "num": 38, "theme": "Courage & audace", 
        "quote": "Essayer quelque chose de nouveau demande du courage, et c'est très bien ainsi.", 
        "quote_he": "לנסות משהו חדש דורש אומץ, וזה בסדר גמור.", 
        "challenge": "Quelle nouvelle habitude ou activité positive aimerais-tu oser tester la semaine prochaine ?"
    },
    {
        "num": 39, "theme": "Courage & audace", 
        "quote": "Dire calmement ce que l'on pense est déjà une force.", 
        "quote_he": "לומר בשקט מה שחושבים זו כבר עוצמה.", 
        "challenge": "Comment exprimer une opinion opposée à celle des autres tout en restant calme ? Écris un exemple de phrase respectueuse."
    },
    {
        "num": 40, "theme": "Courage & audace", 
        "quote": "On grandit chaque fois qu'on ose sortir de sa zone de confort.", 
        "quote_he": "אנחנו גדלים בכל פעם שאנחנו מעזים לצאת מאזור הנוחות.", 
        "challenge": "Écris une action simple qui se situe juste en dehors de ta zone de confort habituelle (ex: aller parler à un nouvel élève)."
    },

    # Gratitude & positivité (41-45)
    {
        "num": 41, "theme": "Gratitude & positivité", 
        "quote": "Prendre le temps de dire merci change une relation.", 
        "quote_he": "להקדיש רגע להגיד תודה יכול לשנות קשר.", 
        "challenge": "Rédige ici un petit message de gratitude chaleureux pour un camarade de classe ou pour un enseignant."
    },
    {
        "num": 42, "theme": "Gratitude & positivité", 
        "quote": "Chaque jour contient au moins une bonne raison de sourire.", 
        "quote_he": "בכל יום יש לפחות סיבה טובה אחת לחייך.", 
        "challenge": "Trouve et note trois petites choses positives (même minuscules) qui se sont passées aujourd'hui dans ta journée."
    },
    {
        "num": 43, "theme": "Gratitude & positivité", 
        "quote": "Voir le positif ne veut pas dire ignorer le difficile.", 
        "quote_he": "לראות את הצד החיובי לא אומר להתעלם מהקושי.", 
        "challenge": "Pense à une situation un peu embêtante de ta journée et essaie de trouver un point positif ou une leçon à en tirer."
    },
    {
        "num": 44, "theme": "Gratitude & positivité", 
        "quote": "La gratitude rend ce que l'on a suffisant.", 
        "quote_he": "הכרת תודה הופכת את מה שיש לך למספיק.", 
        "challenge": "Écris pourquoi tu es reconnaissant(e) d'avoir ton jouet, ton livre ou ton repas préféré aujourd'hui."
    },
    {
        "num": 45, "theme": "Gratitude & positivité", 
        "quote": "Remarquer les efforts des autres, c'est déjà un cadeau.", 
        "quote_he": "לשים לב למאמצים של אחרים זו כבר מתנה.", 
        "challenge": "Quel effort as-tu remarqué chez un camarade de classe, tes parents ou ton enseignant aujourd'hui ? Écris-le pour lui rendre hommage."
    },

    # Respect & écoute (46-50)
    {
        "num": 46, "theme": "Respect & écoute", 
        "quote": "Écouter vraiment, c'est offrir toute son attention.", 
        "quote_he": "להקשיב באמת זה לתת את כל תשומת הלב.", 
        "challenge": "Aujourd'hui, quand un camarade ou l'enseignant te parle, regarde-le attentivement sans penser à autre chose. Raconte comment s'est passée cette connexion."
    },
    {
        "num": 47, "theme": "Respect & écoute", 
        "quote": "Le respect commence par laisser l'autre finir sa phrase.", 
        "quote_he": "כבוד מתחיל בכך שנותנים לאחר לסיים את המשפט שלו.", 
        "challenge": "Aujourd'hui, fais l'effort conscient de ne couper la parole à personne. Est-ce que c'était facile ou difficile pour toi ?"
    },
    {
        "num": 48, "theme": "Respect & écoute", 
        "quote": "On peut ne pas être d'accord et rester respectueux.", 
        "quote_he": "אפשר לא להסכים ובכל זאת להישאר מכבדים.", 
        "challenge": "Imagine que tu n'es pas d'accord sur les règles d'un jeu. Écris une phrase respectueuse pour l'expliquer calmement à ton ami."
    },
    {
        "num": 49, "theme": "Respect & écoute", 
        "quote": "Chaque avis mérite d'être entendu avant d'être discuté.", 
        "quote_he": "כל דעה ראויה להישמע לפני שדנים בה.", 
        "challenge": "Pourquoi est-il enrichissant de connaître l'avis des autres même si tu penses détenir la vérité ?"
    },
    {
        "num": 50, "theme": "Respect & écoute", 
        "quote": "Le silence, parfois, est la meilleure façon d'écouter.", 
        "quote_he": "לפעמים, השתיקה היא הדרך הכי טובה להקשיב.", 
        "challenge": "Ferme les yeux pendant 30 secondes en classe ou chez toi. Quels bruits as-tu découverts en écoutant le silence ? Note-les."
    },

    # Créativité & imagination (51-55)
    {
        "num": 51, "theme": "Créativité & imagination", 
        "quote": "Il n'y a pas une seule bonne façon de résoudre un problème.", 
        "quote_he": "אין רק דרך אחת נכונה לפתור בעיה.", 
        "challenge": "Trouve et écris trois utilisations complètement insolites et drôles pour un simple crayon à papier !"
    },
    {
        "num": 52, "theme": "Créativité & imagination", 
        "quote": "L'imagination transforme une feuille blanche en univers.", 
        "quote_he": "הדמיון הופך דף ריק ליקום שלם.", 
        "challenge": "Ferme les yeux. Imagine une île magique. Décris ce que l'on y trouve de surprenant en deux phrases."
    },
    {
        "num": 53, "theme": "Créativité & imagination", 
        "quote": "Oser une idée originale, c'est déjà créer.", 
        "quote_he": "להעז avec un רעיון מקורי זה כבר ליצור.", 
        "challenge": "Partage une idée créative un peu fofolle que tu as eue récemment, même si elle te paraissait impossible à réaliser !"
    },
    {
        "num": 54, "theme": "Créativité & imagination", 
        "quote": "Se tromper en créant fait partie du processus.", 
        "quote_he": "לטעות תוך כדי יצירה זה חלק מהתהליך.", 
        "challenge": "Raconte un moment où tu as fait un dessin ou un bricolage 'raté' qui s'est finalement transformé en une autre création géniale !"
    },
    {
        "num": 55, "theme": "Créativité & imagination", 
        "quote": "Chaque solution inattendue mérite d'être écoutée.", 
        "quote_he": "כל פתרון מפתיע ראוי להישמע.", 
        "challenge": "Quelle règle originale ou idée insolite pourrais-tu inventer pour rendre le jeu de la récréation encore plus amusant ?"
    },

    # Responsabilité & engagement (56-60)
    {
        "num": 56, "theme": "Responsabilité & engagement", 
        "quote": "Ce que tu fais aujourd'hui construit qui tu seras demain.", 
        "quote_he": "מה שאתה עושה היום בונה את מי שתהיה מחר.", 
        "challenge": "Quelle habitude responsable (ranger, lire, s'entraider, trier) aimerais-tu faire grandir chez toi dès aujourd'hui ?"
    },
    {
        "num": 57, "theme": "Responsabilité & engagement", 
        "quote": "Tenir sa parole, c'est se respecter et respecter les autres.", 
        "quote_he": "לעמוד במילה שלך זה לכבד את עצמך ואת האחרים.", 
        "challenge": "Pourquoi est-il important pour toi de tenir tes promesses envers tes camarades et ton enseignant ?"
    },
    {
        "num": 58, "theme": "Responsabilité & engagement", 
        "quote": "Prendre une responsabilité, c'est montrer qu'on grandit.", 
        "quote_he": "לקחת אחריות זה להראות שאתה גדל.", 
        "challenge": "Quelle petite responsabilité de la classe (distribuer, être responsable des plantes, ranger la bibliothèque...) aimerais-tu assurer ? Pourquoi ?"
    },
    {
        "num": 59, "theme": "Responsabilité & engagement", 
        "quote": "Un petit geste responsable peut inspirer tout un groupe.", 
        "quote_he": "מחווה אחראית קטנה יכולה לעורר השראה בקבוצה שלמה.", 
        "challenge": "Quel geste responsable envers la nature ou la classe as-tu fait ou as-tu vu un camarade faire aujourd'hui ?"
    },
    {
        "num": 60, "theme": "Responsabilité & engagement", 
        "quote": "S'engager, c'est choisir de faire sa part.", 
        "quote_he": "להתחייב זה לבחור לעשות את החלק שלך.", 
        "challenge": "Écris une action collective que tu t'engages à faire pour que ta classe reste propre, solidaire et chaleureuse."
    }
]

# Initialisation du Session State pour sauvegarder les données de jeu locales
if "journal" not in st.session_state:
    st.session_state.journal = []
if "unlocked_badges" not in st.session_state:
    st.session_state.unlocked_badges = []
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "current_card" not in st.session_state:
    st.session_state.current_card = None

# Interface Utilisateur principale
st.write(f"<div class='main-title'>🌟 L'Éveil en Classe 🌟</div>", unsafe_allow_html=True)
st.write("<div class='subtitle'>Messages Inspirants Bilingues (Français / Hébreu) & Défis Interactifs</div>", unsafe_allow_html=True)

# Demander le prénom au départ de la séance
if not st.session_state.user_name:
    st.info("👋 Bonjour ! Entre ton prénom pour commencer l'aventure de l'Éveil en Classe. / שלום! אנא הכנס את שמך כדי להתחיל.")
    cols_name = st.columns([3, 1])
    with cols_name[0]:
        name_input = st.text_input("Comment t'appelles-tu ?", placeholder="Ex: Lucas, Sofiane, Noam...", label_visibility="collapsed")
    with cols_name[1]:
        if st.button("Valider 🚀", use_container_width=True):
            if name_input.strip():
                st.session_state.user_name = name_input.strip()
                st.rerun()
            else:
                st.warning("N'oublie pas d'entrer ton prénom !")
    st.stop()

# Barre d'accueil personnalisée
st.write(f"### 🎈 Bienvenue, **{st.session_state.user_name}** !")


# --- COMPOSANT : AFFICHAGE DE LA CARTE ACTIVE EN FOCUS MODE ---
if st.session_state.current_card:
    card = st.session_state.current_card
    info = THEMES_INFO[card["theme"]]
    
    # Bouton retour en haut
    if st.button("⬅️ Retour au menu principal / חזרה לתפריט הראשי", use_container_width=True):
        st.session_state.current_card = None
        if "wheel_theme" in st.session_state:
            del st.session_state["wheel_theme"]
        st.rerun()
        
    # Structure visuelle bilingue de la carte en HTML/CSS
    st.markdown(f"""
    <div class="card-container" style="border: 4px solid {info['color']}; background-color: {info['bg_light']};">
        <span class="card-header-badge" style="background-color: {info['color']}; color: white;">
            {info['icon']} {card['theme']}
        </span>
        <div class="card-text">
            « {card['quote']} »
        </div>
        <div class="card-text-hebrew">
            "{card['quote_he']}"
        </div>
        <div class="card-footer-info">
            Carte inspirante N°{card['num']} sur 60
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Défi interactif associé
    st.markdown(f"""
    <div class="challenge-box" style="border-left: 5px solid {info['color']}; background-color: #FAFAFA;">
        <h4 style="margin: 0 0 10px 0; color: {info['color']}; font-family: 'Fredoka One', cursive;">🔥 Ton Défi de l'Éveil :</h4>
        <p style="margin: 0; font-size: 1.1rem; color: #2C3E50;"><b>{card['challenge']}</b></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Saisie de la réflexion
    ref_input = st.text_area("Écris ta réponse ici en français ou en hébreu : / כתוב את תשובתך כאן בעברית או בצרפתית:", placeholder="Je pense que... / אני חושב ש...", height=120)
    
    if st.button("Valider mon Défi ! 🎉", use_container_width=True):
        if len(ref_input.strip()) < 4:
            st.error("Ton défi est précieux ! Écris au moins un mot ou une petite phrase pour le valider. / אנא כתוב לפחות מילה או משפט קצר.")
        else:
            # Sauvegarde dans le journal
            new_entry = {
                "date": datetime.date.today().strftime("%d/%m/%Y"),
                "num": card["num"],
                "theme": card["theme"],
                "quote": card["quote"],
                "quote_he": card["quote_he"],
                "reflection": ref_input.strip()
            }
            
            # Éviter de dupliquer si on clique deux fois
            is_duplicate = False
            for entry in st.session_state.journal:
                if entry["num"] == card["num"] and entry["reflection"] == ref_input.strip():
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                st.session_state.journal.append(new_entry)
            
            # Débloquer le badge correspondant au thème
            if card["theme"] not in st.session_state.unlocked_badges:
                st.session_state.unlocked_badges.append(card["theme"])
                st.balloons()
                st.success(f"🏆 MAGNIFIQUE ! Tu as relevé le défi et débloqué le badge **{info['badge_name']}** ! Va le voir dans ton Tableau des Badges !")
            else:
                st.balloons()
                st.success("🎉 Félicitations ! Ta réflexion a bien été ajoutée à ton Journal de l'Éveil !")
            
            # Réinitialiser la carte pour encourager un autre tour si l'élève le souhaite
            st.session_state.current_card = None
            if "wheel_theme" in st.session_state:
                del st.session_state["wheel_theme"]
            time.sleep(1)
            st.rerun()
            
    st.stop()

# Les Onglets de l'Application
tab_game, tab_wheel, tab_badges, tab_journal, tab_teacher = st.tabs([
    "🎲 Tirer une Carte", 
    "🎡 La Roue de l'Éveil",
    "🏆 Mes Badges", 
    "📓 Mon Journal d'Éveil", 
    "🏫 Espace Enseignant"
])

# --- ONGLETS 1 : TIRER UNE CARTE ---
with tab_game:
    st.markdown("### Choisis ton mode de tirage : / בחר את סוג ההגרלה:")
    
    cols_draw = st.columns(2)
    with cols_draw[0]:
        st.markdown("**🍀 Le hasard complet / הגרלה אקראית**")
        if st.button("🎲 Tirer au sort une carte", use_container_width=True):
            st.session_state.current_card = random.choice(CARDS_DATA)
            st.session_state.challenge_validated = False
            st.rerun()
            
    with cols_draw[1]:
        st.markdown("**🎨 Choisir par Thème / בחר לפי נושא**")
        theme_selected = st.selectbox("Choisis ton thème favori :", list(THEMES_INFO.keys()), label_visibility="collapsed")
        if st.button("🔍 Tirer une carte de ce thème", use_container_width=True):
            theme_cards = [c for c in CARDS_DATA if c["theme"] == theme_selected]
            st.session_state.current_card = random.choice(theme_cards)
            st.session_state.challenge_validated = False
            st.rerun()

# --- ONGLETS 2 : LA ROUE DE L'ÉVEIL ---
with tab_wheel:
    st.markdown("### 🎡 Lance la Roue Magique de l'Éveil !")
    st.write("Fais tourner la roue virtuelle pour choisir ensemble le thème de discussion du jour en classe entière !")
    
    if st.button("🌀 Lancer la Roue de l'Éveil !", use_container_width=True):
        spin_placeholder = st.empty()
        themes_list = list(THEMES_INFO.keys())
        
        # Simulation d'un effet de roulement visuel
        for i in range(15):
            t_name = random.choice(themes_list)
            t_info = THEMES_INFO[t_name]
            spin_placeholder.markdown(f"""
            <div style="text-align: center; padding: 40px; background-color: {t_info['bg_light']}; border: 4px dashed {t_info['color']}; border-radius: 20px;">
                <span style="font-size: 5rem;">{t_info['icon']}</span>
                <h2 style="color: {t_info['color']}; font-family: 'Fredoka One', cursive; margin-top: 15px;">{t_name}</h2>
            </div>
            """, unsafe_allow_html=True)
            time.sleep(0.08 + (i * 0.03)) # Décélération progressive
            
        # Sélection finale
        selected_theme = random.choice(themes_list)
        final_info = THEMES_INFO[selected_theme]
        
        spin_placeholder.markdown(f"""
        <div style="text-align: center; padding: 40px; background-color: {final_info['bg_light']}; border: 5px solid {final_info['color']}; border-radius: 20px; box-shadow: 0 10px 20px rgba(0,0,0,0.1);">
            <span style="font-size: 6rem;">🎉 {final_info['icon']} 🎉</span>
            <h1 style="color: {final_info['color']}; font-family: 'Fredoka One', cursive; margin-top: 20px;">{selected_theme}</h1>
            <p style="color: #7F8C8D; font-size: 1.2rem;">Le thème parfait pour aujourd'hui !</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.success(f"✨ Le destin a parlé ! Nous allons travailler sur le thème **{selected_theme}** aujourd'hui.")
        
        # Sauvegarder dans le state pour pouvoir cliquer sur le bouton
        st.session_state.wheel_theme = selected_theme

    if "wheel_theme" in st.session_state:
        # Proposer directement de tirer une carte de ce thème
        if st.button(f"👉 Découvrir une carte du thème : {st.session_state.wheel_theme}", use_container_width=True):
            theme_cards = [c for c in CARDS_DATA if c["theme"] == st.session_state.wheel_theme]
            st.session_state.current_card = random.choice(theme_cards)
            st.session_state.challenge_validated = False
            del st.session_state["wheel_theme"]
            st.rerun()

# --- ONGLETS 3 : TABLEAU DES BADGES ---
with tab_badges:
    st.markdown("### 🏆 Ton Tableau de Chasse des Badges de l'Éveil")
    
    # Barre de progression
    unlocked_count = len(st.session_state.unlocked_badges)
    total_badges = len(THEMES_INFO)
    progress_ratio = unlocked_count / total_badges
    
    st.progress(progress_ratio)
    st.write(f"🎯 **Progression :** {unlocked_count} sur {total_badges} badges débloqués !")
    
    if unlocked_count == total_badges:
        st.success("👑 FANTASTIQUE ! Tu es devenu un(e) Maître de l'Éveil de la classe ! Tu as débloqué tous les badges !")

    # Grille des Badges
    st.write("---")
    badge_html = "<div class='badge-grid'>"
    for theme_name, info in THEMES_INFO.items():
        is_unlocked = theme_name in st.session_state.unlocked_badges
        if is_unlocked:
            badge_html += f"""
            <div class="badge-card badge-active">
                <div class="badge-icon">{info['icon']}</div>
                <div class="badge-title" style="color: {info['color']};">{info['badge_name']}</div>
                <div style="font-size: 0.75rem; color: #7F8C8D; margin-top: 5px;">{info['badge_desc']}</div>
                <div style="font-size: 0.7rem; font-weight: bold; color: #2ECC71; margin-top: 5px;">Débloqué !</div>
            </div>
            """
        else:
            badge_html += f"""
            <div class="badge-card" style="opacity: 0.5;">
                <div class="badge-icon" style="filter: grayscale(100%);">🔒</div>
                <div class="badge-title" style="color: #7F8C8D;">{theme_name}</div>
                <div style="font-size: 0.75rem; color: #BDC3C7; margin-top: 5px;">Fais un défi de ce thème pour l'ouvrir.</div>
            </div>
            """
    badge_html += "</div>"
    st.markdown(badge_html, unsafe_allow_html=True)

# --- ONGLETS 4 : MON JOURNAL D'ÉVEIL ---
with tab_journal:
    st.markdown("### 📓 Ton Journal Personnel des Réflexions")
    st.write("Retrouve ici tout l'historique de tes pensées inspirantes et de tes actions de classe.")
    
    if not st.session_state.journal:
        st.warning("Ton journal est vide pour le moment. Tire une carte et relève ton premier défi pour l'inaugurer ! 📝")
    else:
        # Affichage chronologique inversé (les plus récents en premier)
        for i, entry in enumerate(reversed(st.session_state.journal)):
            info = THEMES_INFO[entry["theme"]]
            st.markdown(f"""
            <div style="background-color: #FFFFFF; border-radius: 15px; padding: 20px; border-left: 6px solid {info['color']}; margin-bottom: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.03);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <span style="font-weight: bold; color: {info['color']}; font-size: 1rem;">{info['icon']} {entry['theme']} - Carte N°{entry['num']}</span>
                    <span style="color: #BDC3C7; font-size: 0.85rem;">🗓️ Fait le {entry['date']}</span>
                </div>
                <p style="font-style: italic; color: #7F8C8D; border-left: 3px solid #ECF0F1; padding-left: 10px; margin: 10px 0;">"{entry['quote']}"</p>
                <p style="font-style: italic; color: #7F8C8D; border-left: 3px solid #ECF0F1; padding-left: 10px; margin: 10px 0; direction: rtl; text-align: right;">"{entry['quote_he']}"</p>
                <div style="background-color: #F8F9F9; padding: 12px; border-radius: 8px; margin-top: 10px;">
                    <p style="margin: 0; font-weight: bold; font-size: 0.95rem; color: #2C3E50;">Ta réflexion :</p>
                    <p style="margin: 5px 0 0 0; color: #34495E; font-size: 1.05rem; white-space: pre-wrap;">{entry['reflection']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Option d'exportation du journal
        st.write("---")
        st.markdown("#### 📥 Exporter mon Journal pour mon Enseignant(e)")
        st.write("Tu peux télécharger toutes tes réponses dans un fichier pour l'envoyer à ton maître ou ta maîtresse, ou simplement l'imprimer !")
        
        journal_text = f"JOURNAL D'ÉVEIL DE : {st.session_state.user_name}\n"
        journal_text += f"Généré le : {datetime.date.today().strftime('%d/%m/%Y')}\n"
        journal_text += "="*50 + "\n\n"
        
        for entry in st.session_state.journal:
            journal_text += f"Date : {entry['date']}\n"
            journal_text += f"Thème : {entry['theme']} (Carte N°{entry['num']})\n"
            journal_text += f"Message inspirant (FR) : \"{entry['quote']}\"\n"
            journal_text += f"Message inspirant (HE) : \"{entry['quote_he']}\"\n"
            journal_text += f"Réflexion de {st.session_state.user_name} :\n{entry['reflection']}\n"
            journal_text += "-"*50 + "\n\n"
            
        st.download_button(
            label="💾 Télécharger mon journal (.txt)",
            data=journal_text,
            file_name=f"journal_eveil_{st.session_state.user_name.lower()}.txt",
            mime="text/plain",
            use_container_width=True
        )

# --- ONGLETS 5 : ESPACE ENSEIGNANT ---
with tab_teacher:
    st.markdown("### 🏫 Mode d'emploi et Usages Pédagogiques (Bilingue)")
    st.write("Chers enseignants, voici comment tirer le meilleur parti de cette application interactive avec vos élèves bilingues :")
    
    st.markdown("""
    #### 🌟 Intégration de l'Hébreu (Bilinguisme)
    * **Cartes bilingues :** Chaque carte affiche désormais le message inspirant en français **ET** sa traduction officielle en hébreu (issue du deck bilingue).
    * **Saisie libre :** Les élèves peuvent rédiger leurs réponses de défi en français, en hébreu ou en mélangeant les deux selon leur aisance.
    
    #### 1. Le Rituel du Matin (Collectif)
    * **Le jeu :** Projetez l'application au tableau (TBI / VPI). Allez sur l'onglet **Roue de l'Éveil** et lancez-la pour tirer un thème. 
    * **L'échange bilingue :** Lisez les deux versions de la carte tirée. C'est un excellent moyen de renforcer le vocabulaire dans les deux langues tout en initiant une discussion positive.
    
    #### 2. Travail en Autonomie (Individuel sur Tablette/iPad/Téléphone)
    * **Le suivi :** Les élèves réalisent les défis de manière autonome et téléchargent leur journal de bord à la fin de la séance pour vous l'envoyer.
    """)
    
    st.info("💡 **Conseil d'utilisation :** Les données de cette application sont stockées localement dans le navigateur de l'appareil (Session State). Pensez à rappeler aux élèves d'export leur journal à la fin d'une séance de travail si vous souhaitez l'évaluer !")
        margin-bottom: 30px;
    }
    
    /* Style de la carte virtuelle */
    .card-container {
        background-color: #FFFFFF;
        border-radius: 25px;
        padding: 35px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.08);
        text-align: center;
        margin: 20px auto;
        max-width: 500px;
        transition: transform 0.3s ease;
    }
    
    .card-container:hover {
        transform: translateY(-5px);
    }
    
    .card-header-badge {
        font-size: 0.9rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 2px;
        padding: 6px 15px;
        border-radius: 50px;
        display: inline-block;
        margin-bottom: 20px;
    }
    
    .card-text {
        font-family: 'Quicksand', sans-serif;
        font-weight: 700;
        font-size: 1.8rem;
        line-height: 1.5;
        color: #2C3E50;
        margin: 30px 0;
        font-style: italic;
    }
    
    .card-footer-info {
        font-size: 0.85rem;
        color: #BDC3C7;
        margin-top: 15px;
        border-top: 1px dashed #ECF0F1;
        padding-top: 15px;
    }
    
    /* Zone de défi */
    .challenge-box {
        background-color: #F9EBEA;
        border-left: 5px solid #E74C3C;
        border-radius: 8px;
        padding: 15px;
        margin: 20px 0;
        font-size: 1.1rem;
    }
    
    /* Badges */
    .badge-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
        gap: 15px;
        margin-top: 20px;
    }
    
    .badge-card {
        background-color: #F8F9F9;
        border: 2px solid #E5E8E8;
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .badge-active {
        background-color: #E8F8F5;
        border: 2px solid #2ECC71;
        box-shadow: 0 5px 15px rgba(46, 204, 113, 0.15);
    }
    
    .badge-icon {
        font-size: 2.2rem;
        margin-bottom: 8px;
    }
    
    .badge-title {
        font-weight: 700;
        font-size: 0.9rem;
        color: #34495E;
    }
</style>
""", unsafe_allow_html=True)

# Définition des données du jeu (les 12 thèmes, couleurs, icônes, badges et les 60 cartes)
THEMES_INFO = {
    "Effort & persévérance": {
        "color": "#E67E22", "bg_light": "#FDF2E9", "icon": "⛰️", 
        "badge_name": "Sommet d'Or", "badge_desc": "Pour ta constance et tes efforts continus."
    },
    "Erreur & apprentissage": {
        "color": "#F1C40F", "bg_light": "#FEF9E7", "icon": "💡", 
        "badge_name": "L'Étincelle", "badge_desc": "Pour avoir transformé une erreur en leçon."
    },
    "Coopération & entraide": {
        "color": "#1ABC9C", "bg_light": "#E8F8F5", "icon": "🤝", 
        "badge_name": "L'Alliance", "badge_desc": "Pour avoir additionné tes forces en groupe."
    },
    "Inclusion & diversité": {
        "color": "#9B59B6", "bg_light": "#F5EEF8", "icon": "🌈", 
        "badge_name": "Arc-en-Ciel", "badge_desc": "Pour avoir célébré la richesse du groupe."
    },
    "Bienveillance & gentillesse": {
        "color": "#FF6B81", "bg_light": "#FFEFF1", "icon": "❤️", 
        "badge_name": "Grand Cœur", "badge_desc": "Pour avoir offert de la douceur ou un sourire."
    },
    "Confiance en soi": {
        "color": "#F39C12", "bg_light": "#FEF5E7", "icon": "⭐", 
        "badge_name": "Étoile Intérieure", "badge_desc": "Pour être fier(e) de toi sans chercher la perfection."
    },
    "Curiosité & apprentissage": {
        "color": "#3498DB", "bg_light": "#EBF5FB", "icon": "🔍", 
        "badge_name": "Explorateur", "badge_desc": "Pour avoir posé des questions et cherché à savoir."
    },
    "Courage & audace": {
        "color": "#E74C3C", "bg_light": "#FDEDEC", "icon": "⚡", 
        "badge_name": "Lion Courageux", "badge_desc": "Pour avoir osé sortir de ta zone de confort."
    },
    "Gratitude & positivité": {
        "color": "#FF9F43", "bg_light": "#FFF3E6", "icon": "☀️", 
        "badge_name": "Rayon de Soleil", "badge_desc": "Pour avoir remarqué les belles choses de ton jour."
    },
    "Respect & écoute": {
        "color": "#2ECC71", "bg_light": "#EAF2F8", "icon": "💬", 
        "badge_name": "Havre de Paix", "badge_desc": "Pour ton écoute attentive et respectueuse."
    },
    "Créativité & imagination": {
        "color": "#8E44AD", "bg_light": "#F4ECF7", "icon": "🎨", 
        "badge_name": "Créateur d'Univers", "badge_desc": "Pour avoir osé une idée inattendue et originale."
    },
    "Responsabilité & engagement": {
        "color": "#27AE60", "bg_light": "#E8F8F5", "icon": "🌱", 
        "badge_name": "Jeune Pousse", "badge_desc": "Pour avoir choisi de faire ta part activement."
    }
}

# Les 60 cartes du deck
CARDS_DATA = [
    # Effort & persévérance (1-5)
    {"num": 1, "theme": "Effort & persévérance", "quote": "Ce n'est pas la vitesse qui compte, c'est la constance.", "challenge": "Pense à une activité que tu as apprise lentement, mais sûrement. Écris-la ici."},
    {"num": 2, "theme": "Effort & persévérance", "quote": "Un effort répété vaut mieux qu'un talent qui abandonne.", "challenge": "Nomme une chose que tu as réussie uniquement en essayant plusieurs fois."},
    {"num": 3, "theme": "Effort & persévérance", "quote": "Tomber fait partie du chemin, se relever fait la différence.", "challenge": "Raconte un moment où tu as eu envie de baisser les bras, mais où tu as choisi de continuer."},
    {"num": 4, "theme": "Effort & persévérance", "quote": "Le progrès se construit un jour à la fois.", "challenge": "Quel petit pas peux-tu faire aujourd'hui pour progresser dans la matière de ton choix ?"},
    {"num": 5, "theme": "Effort & persévérance", "quote": "Persévérer, c'est continuer à croire en soi quand c'est difficile.", "challenge": "Écris une phrase d'encouragement que tu pourrais te dire à toi-même lors d'un exercice difficile."},
    
    # Erreur & apprentissage (6-10)
    {"num": 6, "theme": "Erreur & apprentissage", "quote": "Une erreur bien comprise vaut mille leçons apprises par cœur.", "challenge": "Explique une erreur commise récemment à l'école et ce que tu as compris grâce à elle."},
    {"num": 7, "theme": "Erreur & apprentissage", "quote": "Se tromper, c'est la preuve que tu essaies vraiment.", "challenge": "Célèbre une erreur aujourd'hui ! Écris : 'Aujourd'hui, je me suis trompé(e) sur ... et c'est super car j'ai compris ...'"},
    {"num": 8, "theme": "Erreur & apprentissage", "quote": "Le cerveau grandit chaque fois qu'il relève un défi.", "challenge": "Quel a été ton plus grand défi intellectuel de la semaine ? Comment ton cerveau a-t-il grandi ?"},
    {"num": 9, "theme": "Erreur & apprentissage", "quote": "Ce que tu ne sais pas encore, tu peux l'apprendre demain.", "challenge": "Y a-t-il quelque chose qui te paraît difficile aujourd'hui ? Écris : 'Je ne sais pas encore faire ..., mais je vais l'apprendre !'"},
    {"num": 10, "theme": "Erreur & apprentissage", "quote": "Douter n'est pas un problème, c'est le début de la compréhension.", "challenge": "Pose par écrit une question sur un sujet qui te fait douter ou t'intrigue."},

    # Coopération & entraide (11-15)
    {"num": 11, "theme": "Coopération & entraide", "quote": "À plusieurs, une idée devient un projet.", "challenge": "Pense à un projet que tu aimerais faire avec tes camarades. Décris-le brièvement."},
    {"num": 12, "theme": "Coopération & entraide", "quote": "Aider quelqu'un, c'est aussi apprendre de lui.", "challenge": "Raconte un moment où tu as aidé un camarade et où cela t'a fait du bien ou t'a appris quelque chose."},
    {"num": 13, "theme": "Coopération & entraide", "quote": "Une classe forte est une classe qui s'écoute.", "challenge": "Qu'est-ce que bien écouter signifie pour toi ? Écris une action concrète d'écoute pour aujourd'hui."},
    {"num": 14, "theme": "Coopération & entraide", "quote": "Personne ne réussit vraiment seul.", "challenge": "Remercie par écrit un camarade ou un adulte de l'école qui t'a aidé(e) récemment."},
    {"num": 15, "theme": "Coopération & entraide", "quote": "Travailler ensemble, c'est additionner nos forces.", "challenge": "Quelle est ta 'super-force' (ex: le dessin, l'organisation, le calcul, le calme) que tu peux partager avec un groupe ?"},

    # Inclusion & diversité (16-20)
    {"num": 16, "theme": "Inclusion & diversité", "quote": "Nos différences sont ce qui rend le groupe complet.", "challenge": "Trouve un camarade qui a un goût ou une passion différente des tiennes. Écris ce que cela t'apporte de différent."},
    {"num": 17, "theme": "Inclusion & diversité", "quote": "Il y a plusieurs façons d'être intelligent, et toutes comptent.", "challenge": "Selon toi, quelles sont tes deux formes d'intelligence préférées (manuelle, logique, artistique, sportive, écoute...) ?"},
    {"num": 18, "theme": "Inclusion & diversité", "quote": "Personne n'est un invité ici, tout le monde est chez soi.", "challenge": "Écris un petit geste simple pour que chaque élève se sente bienvenu dans la classe."},
    {"num": 19, "theme": "Inclusion & diversité", "quote": "Comprendre quelqu'un de différent, c'est agrandir son propre monde.", "challenge": "Raconte une fois où tu as parlé avec quelqu'un d'un milieu ou parcours différent. Qu'as-tu découvert ?"},
    {"num": 20, "theme": "Inclusion & diversité", "quote": "Une classe riche rassemble mille façons différentes d'être soi.", "challenge": "Écris trois mots positifs qui te décrivent uniquement toi, et explique pourquoi c'est une force pour la classe."},

    # Bienveillance & gentillesse (21-25)
    {"num": 21, "theme": "Bienveillance & gentillesse", "quote": "Un mot gentil ne coûte rien et peut changer une journée.", "challenge": "Écris un mot gentil destiné à quelqu'un dans la classe. Tu pourras aller lui dire après !"},
    {"num": 22, "theme": "Bienveillance & gentillesse", "quote": "Être doux avec les autres n'est jamais un signe de faiblesse.", "challenge": "Pense à une situation où tu as choisi d'être doux et patient au lieu de t'énerver. Comment t'es-tu senti(e) ?"},
    {"num": 23, "theme": "Bienveillance & gentillesse", "quote": "Un sourire donné au bon moment peut tout changer.", "challenge": "Aujourd'hui, relève le défi de sourire sincèrement à trois personnes différentes. Note ce que tu as ressenti."},
    {"num": 24, "theme": "Bienveillance & gentillesse", "quote": "La bienveillance commence par une écoute sincère.", "challenge": "Prends 2 minutes pour écouter un camarade te raconter quelque chose, sans l'interrompre. Écris tes impressions."},
    {"num": 25, "theme": "Bienveillance & gentillesse", "quote": "Prendre soin des autres, c'est aussi prendre soin de soi.", "challenge": "Comment as-tu pris soin de toi aujourd'hui ? (Une pause tranquille, une bonne lecture, un jeu...)"},

    # Confiance en soi (26-30)
    {"num": 26, "theme": "Confiance en soi", "quote": "Tu n'as pas besoin d'être parfait pour être fier de toi.", "challenge": "Écris une action ou une réussite de ta semaine dont tu es fier(e), même si elle n'était pas parfaitement parfaite."},
    {"num": 27, "theme": "Confiance en soi", "quote": "Ta valeur ne dépend pas d'une note.", "challenge": "Quelles sont tes qualités humaines importantes (gentillesse, humour, écoute...) qui ne s'écrivent pas sur un bulletin de notes ?"},
    {"num": 28, "theme": "Confiance en soi", "quote": "Crois en toi, même les jours où c'est difficile.", "challenge": "Visualise un bouclier imaginaire. Écris 3 forces intérieures ou qualités que tu inscrirais dessus pour te protéger du doute."},
    {"num": 29, "theme": "Confiance en soi", "quote": "Ce que tu penses de toi compte plus que ce que les autres en disent.", "challenge": "Écris un compliment sincère que tu te fais à toi-même aujourd'hui."},
    {"num": 30, "theme": "Confiance en soi", "quote": "Tu as le droit de te tromper et de continuer à avancer.", "challenge": "Complète cette phrase : 'Si j'étais certain(e) de ne pas échouer, la première chose que j'essaierais de faire serait de...'"},

    # Curiosité & apprentissage (31-35)
    {"num": 31, "theme": "Curiosité & apprentissage", "quote": "Une question ouvre toujours plus de portes qu'elle n'en ferme.", "challenge": "Écris une grande question sur la vie, la nature, la science ou l'histoire à laquelle tu aimerais trouver une réponse."},
    {"num": 32, "theme": "Curiosité & apprentissage", "quote": "La curiosité is le premier pas vers la découverte.", "challenge": "Quel sujet ou quel livre a attisé ta curiosité cette semaine ? Pourquoi ?"},
    {"num": 33, "theme": "Curiosité & apprentissage", "quote": "Apprendre, c'est accepter de ne pas tout savoir.", "challenge": "Écris pourquoi, selon toi, il est courageux et utile de dire 'Je ne sais pas, mais je vais chercher !'"},
    {"num": 34, "theme": "Curiosité & apprentissage", "quote": "Chaque livre, chaque question, chaque essai t'emmène plus loin.", "challenge": "Nomme un domaine, une culture ou un sport que tu ne connais pas du tout mais que tu serais curieux(se) de découvrir."},
    {"num": 35, "theme": "Curiosité & apprentissage", "quote": "Le savoir se construit petit à petit, comme une maison.", "challenge": "Quelle petite idée ou information nouvelle as-tu apprise aujourd'hui à l'école ou ailleurs ?"},

    # Courage & audace (36-40)
    {"num": 36, "theme": "Courage & audace", "quote": "Le courage, ce n'est pas l'absence de peur, c'est avancer malgré elle.", "challenge": "Raconte un moment de ta vie où tu as eu peur, mais où tu as choisi d'agir quand même."},
    {"num": 37, "theme": "Courage & audace", "quote": "Lever la main quand on n'est pas sûr, c'est déjà un acte de courage.", "challenge": "Aujourd'hui, tente de lever la main en classe pour poser une question ou donner une réponse, même avec un doute ! Décris ton ressenti."},
    {"num": 38, "theme": "Courage & audace", "quote": "Essayer quelque chose de nouveau demande du courage, et c'est très bien ainsi.", "challenge": "Quelle nouvelle habitude ou activité positive aimerais-tu oser tester la semaine prochaine ?"},
    {"num": 39, "theme": "Courage & audace", "quote": "Dire calmement ce que l'on pense est déjà une force.", "challenge": "Comment exprimer une opinion opposée à celle des autres tout en restant calme ? Écris un exemple de phrase respectueuse."},
    {"num": 40, "theme": "Courage & audace", "quote": "On grandit chaque fois qu'on ose sortir de sa zone de confort.", "challenge": "Écris une action simple qui se situe juste en dehors de ta zone de confort habituelle (ex: aller parler à un nouvel élève)."},

    # Gratitude & positivité (41-45)
    {"num": 41, "theme": "Gratitude & positivité", "quote": "Prendre le temps de dire merci change une relation.", "challenge": "Rédige ici un petit message de gratitude chaleureux pour un camarade de classe ou pour un enseignant."},
    {"num": 42, "theme": "Gratitude & positivité", "quote": "Chaque jour contient au moins une bonne raison de sourire.", "challenge": "Trouve et note trois petites choses positives (même minuscules) qui se sont passées aujourd'hui dans ta journée."},
    {"num": 43, "theme": "Gratitude & positivité", "quote": "Voir le positif ne veut pas dire ignorer le difficile.", "challenge": "Pense à une situation un peu embêtante de ta journée et essaie de trouver un point positif ou une leçon à en tirer."},
    {"num": 44, "theme": "Gratitude & positivité", "quote": "La gratitude rend ce que l'on a suffisant.", "challenge": "Écris pourquoi tu es reconnaissant(e) d'avoir ton jouet, ton livre ou ton repas préféré aujourd'hui."},
    {"num": 45, "theme": "Gratitude & positivité", "quote": "Remarquer les efforts des autres, c'est déjà un cadeau.", "challenge": "Quel effort as-tu remarqué chez un camarade de classe, tes parents ou ton enseignant aujourd'hui ? Écris-le pour lui rendre hommage."},

    # Respect & écoute (46-50)
    {"num": 46, "theme": "Respect & écoute", "quote": "Écouter vraiment, c'est offrir toute son attention.", "challenge": "Aujourd'hui, quand un camarade ou l'enseignant te parle, regarde-le attentivement sans penser à autre chose. Raconte comment s'est passée cette connexion."},
    {"num": 47, "theme": "Respect & écoute", "quote": "Le respect commence par laisser l'autre finir sa phrase.", "challenge": "Aujourd'hui, fais l'effort conscient de ne couper la parole à personne. Est-ce que c'était facile ou difficile pour toi ?"},
    {"num": 48, "theme": "Respect & écoute", "quote": "On peut ne pas être d'accord et rester respectueux.", "challenge": "Imagine que tu n'es pas d'accord sur les règles d'un jeu. Écris une phrase respectueuse pour l'expliquer calmement à ton ami."},
    {"num": 49, "theme": "Respect & écoute", "quote": "Chaque avis mérite d'être entendu avant d'être discuté.", "challenge": "Pourquoi est-il enrichissant de connaître l'avis des autres même si tu penses détenir la vérité ?"},
    {"num": 50, "theme": "Respect & écoute", "quote": "Le silence, parfois, est la meilleure façon d'écouter.", "challenge": "Ferme les yeux pendant 30 secondes en classe ou chez toi. Quels bruits as-tu découverts en écoutant le silence ? Note-les."},

    # Créativité & imagination (51-55)
    {"num": 51, "theme": "Créativité & imagination", "quote": "Il n'y a pas une seule bonne façon de résoudre un problème.", "challenge": "Trouve et écris trois utilisations complètement insolites et drôles pour un simple crayon à papier !"},
    {"num": 52, "theme": "Créativité & imagination", "quote": "L'imagination transforme une feuille blanche en univers.", "challenge": "Ferme les yeux. Imagine une île magique. Décris ce que l'on y trouve de surprenant en deux phrases."},
    {"num": 53, "theme": "Créativité & imagination", "quote": "Oser une idée originale, c'est déjà créer.", "challenge": "Partage une idée créative un peu fofolle que tu as eue récemment, même si elle te paraissait impossible à réaliser !"},
    {"num": 54, "theme": "Créativité & imagination", "quote": "Se tromper en créant fait partie du processus.", "challenge": "Raconte un moment où tu as fait un dessin ou un bricolage 'raté' qui s'est finalement transformé en une autre création géniale !"},
    {"num": 55, "theme": "Créativité & imagination", "quote": "Chaque solution inattendue mérite d'être écoutée.", "challenge": "Quelle règle originale ou idée insolite pourrais-tu inventer pour rendre le jeu de la récréation encore plus amusant ?"},

    # Responsabilité & engagement (56-60)
    {"num": 56, "theme": "Responsabilité & engagement", "quote": "Ce que tu fais aujourd'hui construit qui tu seras demain.", "challenge": "Quelle habitude responsable (ranger, lire, s'entraider, trier) aimerais-tu faire grandir chez toi dès aujourd'hui ?"},
    {"num": 57, "theme": "Responsabilité & engagement", "quote": "Tenir sa parole, c'est se respecter et respecter les autres.", "challenge": "Pourquoi est-il important pour toi de tenir tes promesses envers tes camarades et ton enseignant ?"},
    {"num": 58, "theme": "Responsabilité & engagement", "quote": "Prendre une responsabilité, c'est montrer qu'on grandit.", "challenge": "Quelle petite responsabilité de la classe (distribuer, être responsable des plantes, ranger la bibliothèque...) aimerais-tu assurer ? Pourquoi ?"},
    {"num": 59, "theme": "Responsabilité & engagement", "quote": "Un petit geste responsable peut inspirer tout un groupe.", "challenge": "Quel geste responsable envers la nature ou la classe as-tu fait ou as-tu vu un camarade faire aujourd'hui ?"},
    {"num": 60, "theme": "Responsabilité & engagement", "quote": "S'engager, c'est choisir de faire sa part.", "challenge": "Écris une action collective que tu t'engages à faire pour que ta classe reste propre, solidaire et chaleureuse."}
]

# Initialisation du Session State pour sauvegarder les données de jeu locales
if "journal" not in st.session_state:
    st.session_state.journal = []
if "unlocked_badges" not in st.session_state:
    st.session_state.unlocked_badges = []
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "current_card" not in st.session_state:
    st.session_state.current_card = None

# Interface Utilisateur principale
st.write(f"<div class='main-title'>🌟 L'Éveil en Classe 🌟</div>", unsafe_allow_html=True)
st.write("<div class='subtitle'>Messages Inspirants & Défis Interactifs pour la classe</div>", unsafe_allow_html=True)

# Demander le prénom au départ de la séance
if not st.session_state.user_name:
    st.info("👋 Bonjour ! Entre ton prénom pour commencer l'aventure de l'Éveil en Classe.")
    cols_name = st.columns([3, 1])
    with cols_name[0]:
        name_input = st.text_input("Comment t'appelles-tu ?", placeholder="Ex: Lucas, Emma, Sofiane...", label_visibility="collapsed")
    with cols_name[1]:
        if st.button("Valider 🚀", use_container_width=True):
            if name_input.strip():
                st.session_state.user_name = name_input.strip()
                st.rerun()
            else:
                st.warning("N'oublie pas d'entrer ton prénom !")
    st.stop()

# Barre d'accueil personnalisée
st.write(f"### 🎈 Bienvenue dans ton espace d'Éveil, **{st.session_state.user_name}** !")

# Les Onglets de l'Application
tab_game, tab_wheel, tab_badges, tab_journal, tab_teacher = st.tabs([
    "🎲 Tirer une Carte", 
    "🎡 La Roue de l'Éveil",
    "🏆 Mes Badges", 
    "📓 Mon Journal d'Éveil", 
    "🏫 Espace Enseignant"
])

# --- ONGLETS 1 : TIRER UNE CARTE ---
with tab_game:
    st.markdown("### Choisis ton mode de tirage :")
    
    cols_draw = st.columns(2)
    with cols_draw[0]:
        st.markdown("**🍀 Le hasard complet**")
        if st.button("🎲 Tirer au sort une carte", use_container_width=True):
            st.session_state.current_card = random.choice(CARDS_DATA)
            st.session_state.challenge_validated = False
            
    with cols_draw[1]:
        st.markdown("**🎨 Choisir par Thème**")
        theme_selected = st.selectbox("Choisis ton thème favori :", list(THEMES_INFO.keys()), label_visibility="collapsed")
        if st.button("🔍 Tirer une carte de ce thème", use_container_width=True):
            theme_cards = [c for c in CARDS_DATA if c["theme"] == theme_selected]
            st.session_state.current_card = random.choice(theme_cards)
            st.session_state.challenge_validated = False

    # Affichage de la carte tirée
    if st.session_state.current_card:
        card = st.session_state.current_card
        info = THEMES_INFO[card["theme"]]
        
        # Structure visuelle de la carte en HTML/CSS
        st.markdown(f"""
        <div class="card-container" style="border: 4px solid {info['color']}; background-color: {info['bg_light']};">
            <span class="card-header-badge" style="background-color: {info['color']}; color: white;">
                {info['icon']} {card['theme']}
            </span>
            <div class="card-text">
                {card['quote']}
            </div>
            <div class="card-footer-info">
                Carte inspirante N°{card['num']} sur 60
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Défi interactif associé
        st.markdown(f"""
        <div class="challenge-box" style="border-left: 5px solid {info['color']}; background-color: #FAFAFA;">
            <h4 style="margin: 0 0 10px 0; color: {info['color']}; font-family: 'Fredoka One', cursive;">🔥 Ton Défi de l'Éveil :</h4>
            <p style="margin: 0; font-size: 1.1rem; color: #2C3E50;"><b>{card['challenge']}</b></p>
        </div>
        """, unsafe_allow_html=True)
        
        # Saisie de la réflexion
        ref_input = st.text_area("Écris ta réponse ici. Partage tes pensées en quelques phrases :", placeholder="Je pense que...", height=120)
        
        if st.button("Valider mon Défi ! 🎉", use_container_width=True):
            if len(ref_input.strip()) < 10:
                st.error("Ton défi est précieux ! Écris au moins une vraie phrase (minimum 10 lettres) pour le valider.")
            else:
                # Sauvegarde dans le journal
                new_entry = {
                    "date": datetime.date.today().strftime("%d/%m/%Y"),
                    "num": card["num"],
                    "theme": card["theme"],
                    "quote": card["quote"],
                    "reflection": ref_input.strip()
                }
                
                # Éviter de dupliquer si on clique deux fois
                is_duplicate = False
                for entry in st.session_state.journal:
                    if entry["num"] == card["num"] and entry["reflection"] == ref_input.strip():
                        is_duplicate = True
                        break
                
                if not is_duplicate:
                    st.session_state.journal.append(new_entry)
                
                # Débloquer le badge correspondant au thème
                if card["theme"] not in st.session_state.unlocked_badges:
                    st.session_state.unlocked_badges.append(card["theme"])
                    st.balloons()
                    st.success(f"🏆 MAGNIFIQUE ! Tu as relevé le défi et débloqué le badge **{info['badge_name']}** ! Va le voir dans ton Tableau des Badges !")
                else:
                    st.balloons()
                    st.success("🎉 Félicitations ! Ta réflexion a bien été ajoutée à ton Journal de l'Éveil !")
                
                # Réinitialiser la carte pour encourager un autre tour si l'élève le souhaite
                st.session_state.current_card = None
                time.sleep(1)
                st.rerun()

# --- ONGLETS 2 : LA ROUE DE L'ÉVEIL ---
with tab_wheel:
    st.markdown("### 🎡 Lance la Roue Magique de l'Éveil !")
    st.write("Fais tourner la roue virtuelle pour choisir ensemble le thème de discussion du jour en classe entière !")
    
    if st.button("🌀 Lancer la Roue de l'Éveil !", use_container_width=True):
        spin_placeholder = st.empty()
        themes_list = list(THEMES_INFO.keys())
        
        # Simulation d'un effet de roulement visuel
        for i in range(15):
            t_name = random.choice(themes_list)
            t_info = THEMES_INFO[t_name]
            spin_placeholder.markdown(f"""
            <div style="text-align: center; padding: 40px; background-color: {t_info['bg_light']}; border: 4px dashed {t_info['color']}; border-radius: 20px;">
                <span style="font-size: 5rem;">{t_info['icon']}</span>
                <h2 style="color: {t_info['color']}; font-family: 'Fredoka One', cursive; margin-top: 15px;">{t_name}</h2>
            </div>
            """, unsafe_allow_html=True)
            time.sleep(0.08 + (i * 0.03)) # Décélération progressive
            
        # Sélection finale
        selected_theme = random.choice(themes_list)
        final_info = THEMES_INFO[selected_theme]
        
        spin_placeholder.markdown(f"""
        <div style="text-align: center; padding: 40px; background-color: {final_info['bg_light']}; border: 5px solid {final_info['color']}; border-radius: 20px; box-shadow: 0 10px 20px rgba(0,0,0,0.1);">
            <span style="font-size: 6rem; animation: pulse 1s infinite;">🎉 {final_info['icon']} 🎉</span>
            <h1 style="color: {final_info['color']}; font-family: 'Fredoka One', cursive; margin-top: 20px;">{selected_theme}</h1>
            <p style="color: #7F8C8D; font-size: 1.2rem;">Le thème parfait pour aujourd'hui !</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.success(f"✨ Le destin a parlé ! Nous allons travailler sur le thème **{selected_theme}** aujourd'hui.")
        
        # Proposer directement de tirer une carte de ce thème
        if st.button("👉 Découvrir la carte du thème tiré", use_container_width=True):
            theme_cards = [c for c in CARDS_DATA if c["theme"] == selected_theme]
            st.session_state.current_card = random.choice(theme_cards)
            st.session_state.challenge_validated = False
            st.rerun()

# --- ONGLETS 3 : TABLEAU DES BADGES ---
with tab_badges:
    st.markdown("### 🏆 Ton Tableau de Chasse des Badges de l'Éveil")
    
    # Barre de progression
    unlocked_count = len(st.session_state.unlocked_badges)
    total_badges = len(THEMES_INFO)
    progress_ratio = unlocked_count / total_badges
    
    st.progress(progress_ratio)
    st.write(f"🎯 **Progression :** {unlocked_count} sur {total_badges} badges débloqués !")
    
    if unlocked_count == total_badges:
        st.success("👑 FANTASTIQUE ! Tu es devenu un(e) Maître de l'Éveil de la classe ! Tu as débloqué tous les badges !")

    # Grille des Badges
    st.write("---")
    badge_html = "<div class='badge-grid'>"
    for theme_name, info in THEMES_INFO.items():
        is_unlocked = theme_name in st.session_state.unlocked_badges
        if is_unlocked:
            badge_html += f"""
            <div class="badge-card badge-active">
                <div class="badge-icon">{info['icon']}</div>
                <div class="badge-title" style="color: {info['color']};">{info['badge_name']}</div>
                <div style="font-size: 0.75rem; color: #7F8C8D; margin-top: 5px;">{info['badge_desc']}</div>
                <div style="font-size: 0.7rem; font-weight: bold; color: #2ECC71; margin-top: 5px;">Débloqué !</div>
            </div>
            """
        else:
            badge_html += f"""
            <div class="badge-card" style="opacity: 0.5;">
                <div class="badge-icon" style="filter: grayscale(100%);">🔒</div>
                <div class="badge-title" style="color: #7F8C8D;">{theme_name}</div>
                <div style="font-size: 0.75rem; color: #BDC3C7; margin-top: 5px;">Fais un défi de ce thème pour l'ouvrir.</div>
            </div>
            """
    badge_html += "</div>"
    st.markdown(badge_html, unsafe_allow_html=True)

# --- ONGLETS 4 : MON JOURNAL D'ÉVEIL ---
with tab_journal:
    st.markdown("### 📓 Ton Journal Personnel des Réflexions")
    st.write("Retrouve ici tout l'historique de tes pensées inspirantes et de tes actions de classe.")
    
    if not st.session_state.journal:
        st.warning("Ton journal est vide pour le moment. Tire une carte et relève ton premier défi pour l'inaugurer ! 📝")
    else:
        # Affichage chronologique inversé (les plus récents en premier)
        for i, entry in enumerate(reversed(st.session_state.journal)):
            info = THEMES_INFO[entry["theme"]]
            st.markdown(f"""
            <div style="background-color: #FFFFFF; border-radius: 15px; padding: 20px; border-left: 6px solid {info['color']}; margin-bottom: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.03);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <span style="font-weight: bold; color: {info['color']}; font-size: 1rem;">{info['icon']} {entry['theme']} - Carte N°{entry['num']}</span>
                    <span style="color: #BDC3C7; font-size: 0.85rem;">🗓️ Fait le {entry['date']}</span>
                </div>
                <p style="font-style: italic; color: #7F8C8D; border-left: 3px solid #ECF0F1; padding-left: 10px; margin: 10px 0;">"{entry['quote']}"</p>
                <div style="background-color: #F8F9F9; padding: 12px; border-radius: 8px; margin-top: 10px;">
                    <p style="margin: 0; font-weight: bold; font-size: 0.95rem; color: #2C3E50;">Ta réflexion :</p>
                    <p style="margin: 5px 0 0 0; color: #34495E; font-size: 1.05rem; white-space: pre-wrap;">{entry['reflection']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Option d'exportation du journal
        st.write("---")
        st.markdown("#### 📥 Exporter mon Journal pour mon Enseignant(e)")
        st.write("Tu peux télécharger toutes tes réponses dans un fichier pour l'envoyer à ton maître ou ta maîtresse, ou simplement l'imprimer !")
        
        journal_text = f"JOURNAL D'ÉVEIL DE : {st.session_state.user_name}\n"
        journal_text += f"Généré le : {datetime.date.today().strftime('%d/%m/%Y')}\n"
        journal_text += "="*50 + "\n\n"
        
        for entry in st.session_state.journal:
            journal_text += f"Date : {entry['date']}\n"
            journal_text += f"Thème : {entry['theme']} (Carte N°{entry['num']})\n"
            journal_text += f"Message inspirant : \"{entry['quote']}\"\n"
            journal_text += f"Réflexion de {st.session_state.user_name} :\n{entry['reflection']}\n"
            journal_text += "-"*50 + "\n\n"
            
        st.download_button(
            label="💾 Télécharger mon journal (.txt)",
            data=journal_text,
            file_name=f"journal_eveil_{st.session_state.user_name.lower()}.txt",
            mime="text/plain",
            use_container_width=True
        )

# --- ONGLETS 5 : ESPACE ENSEIGNANT ---
with tab_teacher:
    st.markdown("### 🏫 Mode d'emploi et Usages Pédagogiques")
    st.write("Chers enseignants, voici comment tirer le meilleur parti de cette application interactive avec vos élèves :")
    
    st.markdown("""
    #### 1. Le Rituel du Matin (Collectif)
    * **Comment faire ?** Projetez l'application au tableau (TBI / VPI) à l'arrivée des élèves.
    * **Le jeu :** Allez sur l'onglet **Roue de l'Éveil**, faites tourner la roue magique devant la classe pour décider du thème. 
    * **L'échange :** Tirez la carte associée et lisez-la ensemble. Laissez les élèves s'exprimer oralement sur le défi proposé pendant 5 minutes. C'est une excellente activité de transition pour démarrer la journée dans le calme et la positivité.
    
    #### 2. Travail en Autonomie (Individuel sur Tablette/iPad/Téléphone)
    * **Comment faire ?** Créez un QR code menant au lien de l'application et affichez-le en classe.
    * **Le jeu :** Les élèves l'utilisent individuellement pendant les temps d'autonomie, après avoir fini un travail, ou lors d'ateliers d'Éducation Socioculturelle (EMC).
    * **Le suivi :** À la fin de la semaine, demandez-leur de télécharger leur fichier journal (via l'onglet **Mon Journal d'Éveil**) et de vous le partager sur votre espace de travail habituel (ENT, Classroom, messagerie de classe) ou de l'imprimer pour enrichir leur portfolio de développement personnel.
    
    #### 3. Débats Philosophiques et Ateliers de Langage
    * **Comment faire ?** Utilisez les thèmes et citations comme inducteurs d'écriture ou de débats.
    * **Exemple d'exercice :** Choisissez une carte difficile, par exemple le N°43 : *« Voir le positif ne veut pas dire ignorer le difficile »*. Demandez aux élèves d'écrire leur réponse à ce défi directement dans l'application, puis organisez un cercle de parole en classe pour confronter les idées.
    """)
    
    st.info("💡 **Conseil d'utilisation de la version en ligne :** Les données de cette application sont stockées localement dans le navigateur de l'appareil (Session State). Si l'élève ferme l'onglet, son journal se réinitialise. Pensez à lui rappeler d'exporter son journal à la fin d'une séance de travail si vous souhaitez l'évaluer !")
