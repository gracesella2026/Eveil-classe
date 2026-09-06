# -*- coding: utf-8 -*-
import streamlit as st
import random
import time
import datetime
import json

def clean_html(html_str):
    if not html_str:
        return ""
    return "\n".join(line.strip() for line in html_str.split("\n"))


# Configuration de la page
st.set_page_config(
    page_title="L'Éveil en Classe - Jeu Interactif",
    page_icon="🎴",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Style CSS personnalisé pour l'ambiance chaleureuse de la classe et le support RTL
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
        margin: 20px 0;
        font-style: italic;
    }
    
    .card-text-hebrew {
        font-family: 'Quicksand', 'Segoe UI', Arial, sans-serif;
        font-weight: 700;
        font-size: 1.6rem;
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
        background-color: #FAFAFA;
        border-radius: 12px;
        padding: 20px;
        margin: 20px 0;
        box-shadow: 0 4px 10px rgba(0,0,0,0.02);
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
        "badge_name": "Sommet d'Or / פסגת הזהב", "badge_desc": "Pour ta constance et tes efforts continus. / על התמדה ומאמץ מתמשך."
    },
    "Erreur & apprentissage": {
        "color": "#F1C40F", "bg_light": "#FEF9E7", "icon": "💡", 
        "badge_name": "L'Étincelle / הניצוץ", "badge_desc": "Pour avoir transformé une erreur en leçon. / על הפיכת טעות לשיעור לחיים."
    },
    "Coopération & entraide": {
        "color": "#1ABC9C", "bg_light": "#E8F8F5", "icon": "🤝", 
        "badge_name": "L'Alliance / הברית", "badge_desc": "Pour avoir additionné tes forces en groupe. / על שילוב כוחות בקבוצה."
    },
    "Inclusion & diversité": {
        "color": "#9B59B6", "bg_light": "#F5EEF8", "icon": "🌈", 
        "badge_name": "Arc-en-Ciel / קשת בענן", "badge_desc": "Pour avoir célébré la richesse du groupe. / על חגיגת העושר והגיוון שבקבוצה."
    },
    "Bienveillance & gentillesse": {
        "color": "#FF6B81", "bg_light": "#FFEFF1", "icon": "❤️", 
        "badge_name": "Grand Cœur / לב גדול", "badge_desc": "Pour avoir offert de la douceur ou un sourire. / על הענקת מילה טובה או חיוך."
    },
    "Confiance en soi": {
        "color": "#F39C12", "bg_light": "#FEF5E7", "icon": "⭐", 
        "badge_name": "Étoile Intérieure / כוכב פנימי", "badge_desc": "Pour être fier(e) de toi sans chercher la perfection. / על גאווה בעצמך ללא חיפוש שלמות."
    },
    "Curiosité & apprentissage": {
        "color": "#3498DB", "bg_light": "#EBF5FB", "icon": "🔍", 
        "badge_name": "Explorateur / חוקר", "badge_desc": "Pour avoir posé des questions et cherché à savoir. / על שאילת שאלות ורצון לדעת."
    },
    "Courage & audace": {
        "color": "#E74C3C", "bg_light": "#FDEDEC", "icon": "⚡", 
        "badge_name": "Lion Courageux / אריה אמיץ", "badge_desc": "Pour avoir osé sortir de ta zone de confort. / על העזה לצאת מאזור הנוחות."
    },
    "Gratitude & positivité": {
        "color": "#FF9F43", "bg_light": "#FFF3E6", "icon": "☀️", 
        "badge_name": "Rayon de Soleil / קרן שמש", "badge_desc": "Pour avoir remarqué les belles choses de ton jour. / על תשומת לב לדברים היפים ביומך."
    },
    "Respect & écoute": {
        "color": "#2ECC71", "bg_light": "#EAF2F8", "icon": "💬", 
        "badge_name": "Havre de Paix / נווה שלום", "badge_desc": "Pour ton écoute attentive et respectueuse. / על הקשבה קשובה ומכבדת."
    },
    "Créativité & imagination": {
        "color": "#8E44AD", "bg_light": "#F4ECF7", "icon": "🎨", 
        "badge_name": "Créateur d'Univers / בורא עולמות", "badge_desc": "Pour avoir osé une idée inattendue et originale. / על העזה להביא רעיון מפתיע ומקורי."
    },
    "Responsabilité & engagement": {
        "color": "#27AE60", "bg_light": "#E8F8F5", "icon": "🌱", 
        "badge_name": "Jeune Pousse / שתיל צעיר", "badge_desc": "Pour avoir choisi de faire ta part activement. / על בחירה לקחת חלק פעיל."
    }
}

# Les 60 cartes du deck avec les citations bilingues français / hébreu et deux choix de défis bilingues
CARDS_DATA = [
    # Effort & persévérance (1-5)
    {
        "num": 1, "theme": "Effort & persévérance", 
        "quote": "Ce n'est pas la vitesse qui compte, c'est la constance.", 
        "quote_he": "לא המהירות קובעת, אלא ההתמדה.",
        "challenge_1_fr": "Pense à une activité que tu as apprise lentement, mais sûrement. Écris-la ici.",
        "challenge_1_he": "חשוב על פעילות שלמדת לאט, אבל בטוח. כתוב אותה כאן.",
        "challenge_2_fr": "Demande à ton voisin de table une chose qu'il a réussi à apprendre lentement cette année.",
        "challenge_2_he": "שאל את השכן שלך לשולחן על דבר אחד שהוא הצליח ללמוד לאט השנה."
    },
    {
        "num": 2, "theme": "Effort & persévérance", 
        "quote": "Un effort répété vaut mieux qu'un talent qui abandonne.", 
        "quote_he": "מאמץ מתמשך שווה יותר מכישרון שמוותר.",
        "challenge_1_fr": "Nomme une chose que tu as réussie uniquement en essayant plusieurs fois.",
        "challenge_1_he": "ציין דבר אחד שהצלחת בו רק לאחר שניסית מספר פעמים.",
        "challenge_2_fr": "Trouve un camarade et encourage-le sincèrement pour un travail ou exercice qu'il trouve difficile aujourd'hui.",
        "challenge_2_he": "מצא חבר לכיתה ועודד אותו מכל הלב על עבודה או תרגיל שהוא מוצא קשה היום."
    },
    {
        "num": 3, "theme": "Effort & persévérance", 
        "quote": "Tomber fait partie du chemin, se relever fait la différence.", 
        "quote_he": "ליפול זה חלק מהדרך, לקום זה מה שעושה את ההבדל.",
        "challenge_1_fr": "Raconte un moment où tu as eu envie de baisser les bras, mais où tu as choisi de continuer.",
        "challenge_1_he": "ספר על רגע שבו רצית לוותר, אבל בחרת להמשיך.",
        "challenge_2_fr": "Partage ton histoire de courage ou de persévérance avec ton voisin de classe.",
        "challenge_2_he": "שתף את סיפור האומץ או ההתמדה שלך עם השכן שלך לכיתה."
    },
    {
        "num": 4, "theme": "Effort & persévérance", 
        "quote": "Le progrès se construit un jour à la fois.", 
        "quote_he": "התקדמות נבנית יום אחד בכל פעם.",
        "challenge_1_fr": "Quel petit pas peux-tu faire aujourd'hui pour progresser dans la matière ou l'activité de ton choix ?",
        "challenge_1_he": "איזה צעד קטן תוכל לעשות היום כדי להתקדם במקצוע או בפעילות שתבחר?",
        "challenge_2_fr": "Dessine un escalier sur une feuille et écris le petit pas d'aujourd'hui sur la première marche.",
        "challenge_2_he": "צייר מדרגות על דף וכתוב את הצעד הקטן של היום על המדרגה הראשונה."
    },
    {
        "num": 5, "theme": "Effort & persévérance", 
        "quote": "Persévérer, c'est continuer à croire en soi quand c'est difficile.", 
        "quote_he": "להתמיד זה להמשיך להאמין בעצמך גם כשקשה.",
        "challenge_1_fr": "Écris une phrase d'encouragement chaleureuse que tu pourrais te répéter lors d'un exercice difficile.",
        "challenge_1_he": "כתוב משפט עידוד חם שתוכל להגיד לעצמך במהלך תרגיל קשה.",
        "challenge_2_fr": "Inscris ton mot d'encouragement sur un bout de papier et propose à un camarade de le lire à haute voix.",
        "challenge_2_he": "כתוב את מילת העידוד שלך על פיסת נייר והצע לחבר לקרוא אותה בקול רם."
    },
    
    # Erreur & apprentissage (6-10)
    {
        "num": 6, "theme": "Erreur & apprentissage", 
        "quote": "Une erreur bien comprise vaut mille leçons apprises par cœur.", 
        "quote_he": "טעות שמבינים אותה שווה יותר מאלף שיעורים שלמדו בעל פה.",
        "challenge_1_fr": "Explique une erreur commise récemment à l'école et la leçon précieuse que tu as apprise grâce à elle.",
        "challenge_1_he": "הסבר טעות שעשית לאחרונה בבית הספר ואת השיעור היקר שלמדת בזכותה.",
        "challenge_2_fr": "Explique cette erreur à ton binôme et écoutez ensemble ce que chacun en a retiré de positif.",
        "challenge_2_he": "הסבר את הטעות הזו לחבר שלך לצוות והקשיבו יחד למה שכל אחד מכם הפיק ממנה באופן חיובי."
    },
    {
        "num": 7, "theme": "Erreur & apprentissage", 
        "quote": "Se tromper, c'est la preuve que tu essaies vraiment.", 
        "quote_he": "לטעות זו ההוכחה שאתה באמת מנסה.",
        "challenge_1_fr": "Célèbre une erreur aujourd'hui ! Écris : 'Aujourd'hui, je me suis trompé(e) sur ... et c'est super car j'ai compris ...'",
        "challenge_1_he": "חגוג טעות היום! כתוב: 'היום טעיתי ב... וזה נהדר כי הבנתי ש...'",
        "challenge_2_fr": "Lève les mains en l'air et dis joyeusement : 'Je grandis !' avec ton voisin de table pour dédramatiser les erreurs.",
        "challenge_2_he": "הרם ידיים באוויר ואמור בשמחה: 'אני צומח!' יחד עם השכן שלך לשולחן כדי להפחית את הפחד מטעויות."
    },
    {
        "num": 8, "theme": "Erreur & apprentissage", 
        "quote": "Le cerveau grandit chaque fois qu'il relève un défi.", 
        "quote_he": "המוח גדל בכל פעם שהוא מתמודד עם אתגר.",
        "challenge_1_fr": "Quel a été ton plus grand défi intellectuel de la semaine ? Comment ton cerveau s'est-il musclé ?",
        "challenge_1_he": "מה היה האתגר המחשבתי הכי גדול שלך השבוע? איך המוח שלך התחזק?",
        "challenge_2_fr": "Fais un mime amusant de musculation du cerveau devant tes camarades de table.",
        "challenge_2_he": "עשה פנטומימה משעשעת של אימון שרירי המוח מול החברים שלך לשולחן."
    },
    {
        "num": 9, "theme": "Erreur & apprentissage", 
        "quote": "Ce que tu ne sais pas encore, tu peux l'apprendre demain.", 
        "quote_he": "מה שאתה עוד לא יודע, תוכל ללמוד מחר.",
        "challenge_1_fr": "Y a-t-il quelque chose qui te paraît trop difficile aujourd'hui ? Écris : 'Je ne sais pas encore faire ..., mais je vais l'apprendre !'",
        "challenge_1_he": "האם יש משהו שנראה לך קשה מדי היום? כתוב: 'אני עדיין לא יודע איך לעשות..., אבל אני אלמד!'",
        "challenge_2_fr": "Va voir un camarade qui sait faire cette activité et demande-lui s'il peut te montrer un petit secret de réussite.",
        "challenge_2_he": "לך לחבר שיודע לעשות את הפעילות הזו ובקש ממנו להראות לך סוד קטן להצלחה."
    },
    {
        "num": 10, "theme": "Erreur & apprentissage", 
        "quote": "Douter n'est pas un problème, c'est le début de la compréhension.", 
        "quote_he": "לפקפק זה לא בעיה, זו ההתחלה של ההבנה.",
        "challenge_1_fr": "Pose par écrit une grande question sur un sujet de classe qui te fait douter ou t'intrigue beaucoup.",
        "challenge_1_he": "כתוב שאלה גדולה על נושא מהכיתה שמעורר בך ספק או מסקרן אותך מאוד.",
        "challenge_2_fr": "Partage cette question avec ton enseignant ou dépose-la dans la boîte à questions de la classe.",
        "challenge_2_he": "שתף את השאלה הזו עם המורה שלך או הכנס אותה לתיבת השאלות של הכיתה."
    },

    # Coopération & entraide (11-15)
    {
        "num": 11, "theme": "Coopération & entraide", 
        "quote": "À plusieurs, une idée devient un projet.", 
        "quote_he": "יחד, רעיון הופך לפרויקט.",
        "challenge_1_fr": "Pense à un projet créatif ou à un jeu que tu aimerais faire avec tes camarades. Décris-le brièvement.",
        "challenge_1_he": "חשוב על פרויקט יצירתי או משחק שהיית רוצה לעשות עם החברים שלך. תאר אותו בקצר.",
        "challenge_2_fr": "Partage cette idée de projet à voix haute avec deux camarades et notez ensemble une première étape pour le réaliser.",
        "challenge_2_he": "שתף את הרעיון הזה לפרויקט בקול רם עם שני חברים וכתבו יחד צעד ראשון למימושו."
    },
    {
        "num": 12, "theme": "Coopération & entraide", 
        "quote": "Aider quelqu'un, c'est aussi apprendre de lui.", 
        "quote_he": "לעזור למישהו זה גם ללמוד ממנו.",
        "challenge_1_fr": "Raconte un moment récent où tu as aidé un camarade et explique ce que cela t'a appris ou le bien que cela t'a fait.",
        "challenge_1_he": "ספר על רגע לאחרונה שבו עזרת לחבר והסבר מה זה לימד אותך או איך זה גרם לך להרגיש טוב.",
        "challenge_2_fr": "Propose une aide concrète à un camarade de classe aujourd'hui (ex: lui prêter un stylo, lui expliquer une consigne).",
        "challenge_2_he": "הצע עזרה מעשית לחבר לכיתה היום (למשל: להשאיל לו עיקרון, להסביר לו הנחיה)."
    },
    {
        "num": 13, "theme": "Coopération & entraide", 
        "quote": "Une classe forte est une classe qui s'écoute.", 
        "quote_he": "כיתה חזקה היא כיתה שמקשיבה לעצמה.",
        "challenge_1_fr": "Qu'est-ce que 'bien écouter' signifie pour toi ? Écris une règle d'or pour une bonne écoute collective.",
        "challenge_1_he": "מה המשמעות של 'להקשיב היטב' עבורך? כתוב כלל זהב להקשבה קבוצתית טובה.",
        "challenge_2_fr": "Pendant le prochain débat ou travail de groupe, regarde attentivement chaque personne qui parle sans l'interrompre.",
        "challenge_2_he": "במהלך הדיון או העבודה הקבוצתית הבאה, הבט בריכוז בכל אדם שמדבר מבלי לקטוע אותו."
    },
    {
        "num": 14, "theme": "Coopération & entraide", 
        "quote": "Personne ne réussit vraiment seul.", 
        "quote_he": "אף אחד לא באמת מצליח לבד.",
        "challenge_1_fr": "Remercie par écrit un camarade ou un adulte de l'école qui t'a apporté son aide ou son soutien récemment.",
        "challenge_1_he": "הבע תודה בכתב לחבר או למבוגר בבית הספר שהגיש לך עזרה או תמיכה לאחרונה.",
        "challenge_2_fr": "Va dire ce merci de vive voix à la personne, ou glisse-lui ton petit mot écrit de façon amicale.",
        "challenge_2_he": "לך להגיד את התודה הזו בעל פה לאותו אדם, או הגש לו את הפתק הקטן בצורה חברותית."
    },
    {
        "num": 15, "theme": "Coopération & entraide", 
        "quote": "Travailler ensemble, c'est additionner nos forces.", 
        "quote_he": "לעבוד ביחד זה לחבר את הכוחות שלנו.",
        "challenge_1_fr": "Quelle est ta 'super-force' personnelle (le dessin, le calme, le calcul, l'écoute) que tu aimes mettre au service de la classe ?",
        "challenge_1_he": "מהו 'כוח-העל' האישי שלך (ציור, רוגע, חישוב, הקשבה) שאתה אוהב להעמיד לטובת הכיתה?",
        "challenge_2_fr": "Forme un binôme et combine ta super-force avec celle de ton voisin pour imaginer un duo de super-héros de l'entraide.",
        "challenge_2_he": "צור צוות עם חבר ושילב את כוח-העל שלך עם שלו כדי לדמיין צמד גיבורי-על של עזרה הדדית."
    },

    # Inclusion & diversité (16-20)
    {
        "num": 16, "theme": "Inclusion & diversité", 
        "quote": "Nos différences sont ce qui rend le groupe complet.", 
        "quote_he": "ההבדלים בינינו הם מה שהופך את הקבוצה לשלמה.",
        "challenge_1_fr": "Trouve un camarade qui a des goûts ou une passion très différents des tiennes. Écris ce que sa différence apporte de riche au groupe.",
        "challenge_1_he": "מצא חבר לכיתה שיש לו טעמים או תחביב שונים מאוד משלך. כתוב מה השוני שלו מוסיף לקבוצה.",
        "challenge_2_fr": "Va lui poser une question sur sa passion pour essayer de comprendre son univers aujourd'hui.",
        "challenge_2_he": "לך לשאול אותו שאלה על התחביב שלו כדי לנסות להבין את עולמו היום."
    },
    {
        "num": 17, "theme": "Inclusion & diversité", 
        "quote": "Il y a plusieurs façons d'être intelligent, et toutes comptent.", 
        "quote_he": "יש כמה דרכים להיות חכם, וכולן חשובות.",
        "challenge_1_fr": "Selon toi, quelles sont tes deux formes d'intelligence préférées (artistique, logique, sportive, manuelle, nature, écoute...) ?",
        "challenge_1_he": "לדעתך, מהן שתי צורות האינטליגנציה המועדפות עליך (אמנותית, לוגית, ספורטיבית, ידנית, טבע, הקשבה...) ?",
        "challenge_2_fr": "Écris sur ton cahier le nom d'un camarade de classe qui brille dans une forme d'intelligence différente de la tienne, et félicite-le.",
        "challenge_2_he": "כתוב במחברת שלך שם של חבר לכיתה שמצטיין בצורת אינטליגנציה שונה משלך, והחמא לו על כך."
    },
    {
        "num": 18, "theme": "Inclusion & diversité", 
        "quote": "Personne n'est un invité ici, tout le monde est chez soi.", 
        "quote_he": "אף אחד כאן הוא לא אורח, כולם בבית.",
        "challenge_1_fr": "Écris un petit geste d'accueil ou une phrase simple pour que chaque élève (nouveau ou timide) se sente bienvenu dans la classe.",
        "challenge_1_he": "כתוב מחווה קטנה של קבלת פנים או משפט פשוט כדי שכל תלמיד (חדש או ביישן) ירגיש רצוי בכיתה.",
        "challenge_2_fr": "Aujourd'hui à la récréation, propose à un camarade isolé ou qui joue seul de se joindre à vos activités.",
        "challenge_2_he": "היום בהפסקה, הצע לחבר בודד או למי שמשחק לבדו להצטרף לפעילויות שלכם."
    },
    {
        "num": 19, "theme": "Inclusion & diversité", 
        "quote": "Comprendre quelqu'un de différent, c'est agrandir son propre monde.", 
        "quote_he": "להבין מישהו שונה ממך זה להרחיב את העולם שלך.",
        "challenge_1_fr": "Raconte une fois où tu as partagé un moment avec quelqu'un d'un autre milieu ou pays. Qu'as-tu découvert de nouveau ?",
        "challenge_1_he": "ספר על פעם שבה שיתפת רגע עם מישהו מרקע או מדינה אחרת. מה גילית מחדש?",
        "challenge_2_fr": "Apprends aujourd'hui à dire 'Bonjour' ou 'Merci' dans une autre langue avec l'aide d'un camarade bilingue de la classe.",
        "challenge_2_he": "למד היום להגיד 'שלום' או 'תודה' בשפה אחרת בעזרת חבר לכיתה הדובר שתי שפות."
    },
    {
        "num": 20, "theme": "Inclusion & diversité", 
        "quote": "Une classe riche rassemble mille façons différentes d'être soi.", 
        "quote_he": "כיתה עשירה מאגדת בתוכה אלף דרכים שונות להיות עצמך.",
        "challenge_1_fr": "Écris trois qualités positives qui te caractérisent, et explique pourquoi ces traits uniques enrichissent ta classe.",
        "challenge_1_he": "כתוב שלוש תכונות חיוביות שמאפיינות אותך, והסבר מדוע התכונות הייחודיות הללו מעשירות את הכיתה שלך.",
        "challenge_2_fr": "Créez une fresque de mots avec vos camarades en écrivant chacun votre principale qualité sur un poster au tableau.",
        "challenge_2_he": "צרו פסיפס מילים עם חבריכם לכיתה על ידי כתיבת התכונה העיקרית של כל אחד מכם על כרזה על הלוח."
    },

    # Bienveillance & gentillesse (21-25)
    {
        "num": 21, "theme": "Bienveillance & gentillesse", 
        "quote": "Un mot gentil ne coûte rien et peut changer une journée.", 
        "quote_he": "מילה טובה לא עולה כלום ויכולה לשנות יום שלם.",
        "challenge_1_fr": "Rédige un petit mot gentil anonyme destiné à un camarade de la classe pour lui souhaiter une belle journée. Décris ce qu'il va ressentir.",
        "challenge_1_he": "כתוב מילה טובה אנונימית המיועדת לחבר לכיתה כדי לאחל לו יום יפה. תאר מה הוא ירגיש.",
        "challenge_2_fr": "Glisse discrètement ton petit mot écrit sur la table de ce camarade pour lui faire une jolie surprise.",
        "challenge_2_he": "הנח בדיסקרטיות את הפתק הקטן שכתבת על השולחן של אותו חבר כדי להפתיע אותו בצורה נעימה."
    },
    {
        "num": 22, "theme": "Bienveillance & gentillesse", 
        "quote": "Être doux avec les autres n'est jamais un signe de faiblesse.", 
        "quote_he": "להיות עדין עם אחרים הוא לעולם לא סימן לחולשה.",
        "challenge_1_fr": "Pense à une situation récente où tu as choisi de répondre avec douceur et calme au lieu de t'énerver. Comment t'es-tu senti(e) ?",
        "challenge_1_he": "חשוב על סיטואציה לאחרונה שבה בחרת להגיב בעדינות וברוגע במקום להתעצבן. איך הרגשת?",
        "challenge_2_fr": "Fais l'exercice de respirer profondément trois fois de suite la prochaine fois que tu ressens de l'agacement ou de l'énervement.",
        "challenge_2_he": "תרגל נשימה עמוקה שלוש פעמים ברציפות בפעם הבאה שאתה מרגיש כעס או תסכול."
    },
    {
        "num": 23, "theme": "Bienveillance & gentillesse", 
        "quote": "Un sourire donné au bon moment peut tout changer.", 
        "quote_he": "חיוך שניתן ברגע הנכון יכול לשנות הכול.",
        "challenge_1_fr": "Aujourd'hui, ton défi est de sourire chaleureusement et sincèrement à trois personnes différentes dans l'école (un camarade, un adulte, un enseignant). Note ce que tu as ressenti.",
        "challenge_1_he": "היום, האתגר שלך הוא לחייך בחמימות ובכנות לשלושה אנשים שונים בבית הספר (חבר, מבוגר, מורה). רשום מה הרגשת.",
        "challenge_2_fr": "Fais un concours de sourires complices en binôme : tenez le regard en souriant sans rire le plus longtemps possible.",
        "challenge_2_he": "עשו תחרות חיוכים שובבים בזוגות: הביטו זה בזה תוך כדי חיוך מבלי לצחוק כמה שיותר זמן."
    },
    {
        "num": 24, "theme": "Bienveillance & gentillesse", 
        "quote": "La bienveillance commence par une écoute sincère.", 
        "quote_he": "טוב לב מתחיל בהקשבה כנה.",
        "challenge_1_fr": "Prends 2 minutes pour écouter un camarade de classe te raconter un projet ou un souvenir, sans l'interrompre une seule fois. Écris tes impressions.",
        "challenge_1_he": "הקדש 2 דקות כדי להקשיב לחבר לכיתה המספר לך על פרויקט או זיכרון, מבלי לקטוע אותו אף לא פעם אחת. כתוב את רשמיך.",
        "challenge_2_fr": "Faites un jeu de miroir en binôme : l'un raconte une petite histoire, l'autre doit ensuite la reformuler exactement avec ses propres mots.",
        "challenge_2_he": "שחקו במשחק מראה בזוגות: אחד מספר סיפור קצר, והשני צריך לנסח אותו מחדש בדיוק במילותיו שלו."
    },
    {
        "num": 25, "theme": "Bienveillance & gentillesse", 
        "quote": "Prendre soin des autres, c'est aussi prendre soin de soi.", 
        "quote_he": "לדאוג לאחרים זה גם לדאוג לעצמך.",
        "challenge_1_fr": "Comment as-tu pris soin de toi aujourd'hui ? (Une pause tranquille, une grande inspiration, une bonne lecture, un jeu apaisant...). Décris ce moment.",
        "challenge_1_he": "איך דאגת לעצמך היום? (הפסקה שקטה, נשימה עמוקה, קריאה טובה, משחק מרגיע...). תאר את הרגע הזה.",
        "challenge_2_fr": "Installe-toi confortablement sur ta chaise, ferme les yeux et détends tous tes muscles pendant une minute complète en classe.",
        "challenge_2_he": "שב בנוח על הכיסא שלך, עצום עיניים והרפה את כל השרירים שלך במשך דקה שלמה בכיתה."
    },

    # Confiance en soi (26-30)
    {
        "num": 26, "theme": "Confiance en soi", 
        "quote": "Tu n'as pas besoin d'être parfait pour être fier de toi.", 
        "quote_he": "אתה לא צריך להיות מושלם כדי להיות גאה בעצמך.",
        "challenge_1_fr": "Écris une action ou une réussite de ta semaine dont tu es fier(e), même si le résultat n'était pas absolument impeccable.",
        "challenge_1_he": "כתוב פעולה או הצלחה מהשבוע שלך שאתה גאה בה, גם אם התוצאה לא הייתה מושלמת לחלוטין.",
        "challenge_2_fr": "Partage cette réussite imparfaite avec la classe ou avec ton voisin de table et célébrez votre effort.",
        "challenge_2_he": "שתף את ההצלחה הלא-מושלמת הזו עם הכיתה או עם השכן שלך לשולחן וחגגו את המאמץ שלכם."
    },
    {
        "num": 27, "theme": "Confiance en soi", 
        "quote": "Ta valeur ne dépend pas d'une note.", 
        "quote_he": "הערך שלך לא נמדד בציון.",
        "challenge_1_fr": "Quelles sont tes qualités humaines fondamentales (générosité, humour, créativité, sens de l'écoute...) qui ne s'écrivent pas sur un bulletin scolaire ?",
        "challenge_1_he": "מהן התכונות האנושיות הבסיסיות שלך (נדיבות, הומור, יצירתיות, יכולת הקשבה...) שלא נכתבות בתעודת בית הספר?",
        "challenge_2_fr": "Écris l'une de tes plus belles qualités sur ton cahier et entoure-la de coeurs et d'étoiles colorés pour la mettre en valeur.",
        "challenge_2_he": "כתוב את אחת התכונות הכי יפות שלך במחברת והקף אותה בלבבות וכוכבים צבעוניים כדי להדגיש אותה."
    },
    {
        "num": 28, "theme": "Confiance en soi", 
        "quote": "Crois en toi, même les jours où c'est difficile.", 
        "quote_he": "תאמין בעצמך, גם בימים הקשים.",
        "challenge_1_fr": "Visualise un bouclier protecteur imaginaire. Écris 3 forces intérieures ou qualités personnelles que tu dessinerais dessus pour éloigner le doute.",
        "challenge_1_he": "דמיין מגן הגנה דמיוני. כתוב 3 כוחות פנימיים או תכונות אישיות שהיית מצייר עליו כדי להרחיק את הספק.",
        "challenge_2_fr": "Dessine ce bouclier des forces sur une feuille de papier et montre-le fièrement à ton enseignant ou à tes camarades.",
        "challenge_2_he": "צייר את מגן הכוחות הזה על דף נייר והראה אותו בגאווה למורה שלך או לחבריך לכיתה."
    },
    {
        "num": 29, "theme": "Confiance en soi", 
        "quote": "Ce que tu penses de toi compte plus que ce que les autres en disent.", 
        "quote_he": "מה שאתה חושב על עצמך חשוב יותר ממה שאחרים אומרים.",
        "challenge_1_fr": "Rédige un compliment sincère et encourageant que tu te fais à toi-même aujourd'hui pour valoriser ton travail.",
        "challenge_1_he": "כתוב מחמאה כנה ומעודדת שאתה נותן לעצמך היום כדי להעריך את העבודה שלך.",
        "challenge_2_fr": "Regarde-toi dans un petit miroir ou imagine ton reflet, et dis-toi ce compliment dans ta tête avec conviction.",
        "challenge_2_he": "הביט בעצמך במראה קטנה או דמיין את ההשתקפות שלך, ואמור לעצמך את המחמאה הזו בראש בביטחון."
    },
    {
        "num": 30, "theme": "Confiance en soi", 
        "quote": "Tu as le droit de te tromper et de continuer à avancer.", 
        "quote_he": "מותר לך לטעות ולהמשיך להתקדם.",
        "challenge_1_fr": "Complète cette phrase avec sincérité : 'Si j'étais certain(e) de ne jamais échouer, la première chose audacieuse que j'essaierais de faire serait de...'",
        "challenge_1_he": "השלם את המשפט הזה בכנות: 'אם הייתי בטוח שלא אכשל לעולם, הדבר הנועז הראשון שהייתי מנסה לעשות היה...'",
        "challenge_2_fr": "Fais un pas physique en avant dans la classe pour symboliser ta décision d'avancer malgré les doutes.",
        "challenge_2_he": "עשה צעד פיזי קדימה בכיתה כדי לסמל את ההחלטה שלך להתקדם למרות הספקות."
    },

    # Curiosité & apprentissage (31-35)
    {
        "num": 31, "theme": "Curiosité & apprentissage", 
        "quote": "Une question ouvre toujours plus de portes qu'elle n'en ferme.", 
        "quote_he": "שאלה תמיד פותחת יותר דלתות משהיא סוגרת.",
        "challenge_1_fr": "Écris une grande question philosophique sur la vie, la nature ou l'espace à laquelle tu aimerais trouver une réponse.",
        "challenge_1_he": "כתוב שאלה פילוסופית גדולה על החיים, הטבע או החלל שהיית רוצה למצוא לה תשובה.",
        "challenge_2_fr": "Pose cette question à ton enseignant ou à tes camarades de table et discutez-en brièvement ensemble.",
        "challenge_2_he": "שאל את השאלה הזו את המורה שלך או את החברים שלך לשולחן ודונו בה בקצרה יחד."
    },
    {
        "num": 32, "theme": "Curiosité & apprentissage", 
        "quote": "La curiosité est le premier pas vers la découverte.", 
        "quote_he": "סקרנות היא הצעד הראשון לגילוי.",
        "challenge_1_fr": "Quel sujet scientifique, historique ou culturel a le plus éveillé ta curiosité cette semaine ? Pourquoi ?",
        "challenge_1_he": "איזה נושא מדעי, היסטורי או תרבותי עורר הכי הרבה את הסקרנות שלך השבוע? מדוע?",
        "challenge_2_fr": "Va chercher un livre ou un dictionnaire dans la bibliothèque de la classe pour y découvrir une information insolite sur ce sujet.",
        "challenge_2_he": "חפש ספר או מילון בספריית הכיתה כדי לגלות מידע מעניין ומפתיע בנושא זה."
    },
    {
        "num": 33, "theme": "Curiosité & apprentissage", 
        "quote": "Apprendre, c'est accepter de ne pas tout savoir.", 
        "quote_he": "ללמוד זה להסכים לא לדעת הכול.",
        "challenge_1_fr": "Écris pourquoi, selon toi, il est courageux et utile de savoir dire 'Je ne sais pas encore, mais je vais chercher !'",
        "challenge_1_he": "כתוב מדוע, לדעתך, זה אמיץ ומועיל לדעת להגיד 'אני עדיין לא יודע, אבל אני אחקור!'",
        "challenge_2_fr": "Entraîne-toi à dire cette phrase bilingue à voix haute avec ton binôme sur un ton joyeux et plein d'énergie.",
        "challenge_2_he": "התאמן על אמירת המשפט הזה בשתי השפות בקול רם עם בן הזוג שלך בטון שמח ומלא אנרגיה."
    },
    {
        "num": 34, "theme": "Curiosité & apprentissage", 
        "quote": "Chaque livre, chaque question, chaque essai t'emmène plus loin.", 
        "quote_he": "כל ספר, כל שאלה, כל ניסיון לוקחים אותך רחוק יותר.",
        "challenge_1_fr": "Nomme un pays, un sport ou un domaine artistique que tu ne connais pas du tout mais que tu serais curieux(se) d'explorer.",
        "challenge_1_he": "ציין מדינה, ספורט או תחום אמנותי שאתה לא מכיר בכלל אבל היית מסוקרן לחקור.",
        "challenge_2_fr": "Dessine la silhouette d'un bateau ou d'une montgolfière et écris ce projet de découverte à l'intérieur.",
        "challenge_2_he": "צייר צללית של סירה או כדור פורח וכתוב את פרויקט הגילוי הזה בפנים."
    },
    {
        "num": 35, "theme": "Curiosité & apprentissage", 
        "quote": "Le savoir se construit petit à petit, comme une maison.", 
        "quote_he": "הידע נבנה לאט לאט, כמו בית.",
        "challenge_1_fr": "Quelle petite information ou idée nouvelle et surprenante as-tu apprise aujourd'hui à l'école ou à la maison ?",
        "challenge_1_he": "איזה מידע קטן או רעיון חדש ומפתיע למדת היום בבית הספר או בבית?",
        "challenge_2_fr": "Dessine une brique sur ton cahier et écris ton savoir du jour dedans pour commencer à bâtir ta maison du savoir.",
        "challenge_2_he": "צייר לבנה במחברת שלך וכתוב את הידע היומי שלך בתוכה כדי להתחיל לבנות את בית הידע שלך."
    },

    # Courage & audace (36-40)
    {
        "num": 36, "theme": "Courage & audace", 
        "quote": "Le courage, ce n'est pas l'absence de peur, c'est avancer malgré elle.", 
        "quote_he": "אומץ הוא לא היעדר פחד, אלא להתקדם למרותו.",
        "challenge_1_fr": "Raconte un moment de ta vie d'enfant où tu as ressenti de la peur ou de l'inquiétude, mais où tu as choisi d'agir courageusement.",
        "challenge_1_he": "ספר על רגע בחייך כילד שבו הרגשת פחד או דאגה, אך בחרת לפעול באומץ.",
        "challenge_2_fr": "Partage cette anecdote de courage avec ton voisin de table pour l'inspirer.",
        "challenge_2_he": "שתף את הסיפור הקטן הזה על אומץ עם השכן שלך לשולחן כדי לתת לו השראה."
    },
    {
        "num": 37, "theme": "Courage & audace", 
        "quote": "Lever la main quand on n'est pas sûr, c'est déjà un acte de courage.", 
        "quote_he": "להרים יד כשלא בטוחים זו כבר פעולה אמיצה.",
        "challenge_1_fr": "Aujourd'hui, tente de lever la main en classe pour donner une réponse ou poser une question, même si tu as un doute. Décris ce que tu as éprouvé.",
        "challenge_1_he": "היום, נסה להרים את היד בכיתה כדי לענות או לשאול שאלה, גם אם יש לך ספק. תאר מה הרגשת.",
        "challenge_2_fr": "Fais le geste physique de lever la main bien haut tout de suite en souriant pour t'entraîner au courage scolaire.",
        "challenge_2_he": "עשה את המחווה הפיזית של הרמת היד גבוה כבר עכשיו תוך כדי חיוך כדי להתאמן על אומץ לימודי."
    },
    {
        "num": 38, "theme": "Courage & audace", 
        "quote": "Essayer quelque chose de nouveau demande du courage, et c'est très bien ainsi.", 
        "quote_he": "לנסות משהו חדש דורש אומץ, וזה בסדר גמור.",
        "challenge_1_fr": "Quelle nouvelle habitude positive ou quelle activité originale aimerais-tu oser tester la semaine prochaine ?",
        "challenge_1_he": "איזה הרגל חיובי חדש או פעילות מקורית היית רוצה להעיז לנסות בשבוע הבא?",
        "challenge_2_fr": "Va proposer un jeu différent à tes camarades de classe lors de la prochaine récréation pour changer de vos habitudes.",
        "challenge_2_he": "לך להציע משחק שונה לחבריך לכיתה במהלך ההפסקה הבאה כדי לשנות את ההרגלים שלכם."
    },
    {
        "num": 39, "theme": "Courage & audace", 
        "quote": "Dire calmement ce que l'on pense est déjà une force.", 
        "quote_he": "לומר בשקט מה שחושבים זו כבר עוצמה.",
        "challenge_1_fr": "Comment exprimer une opinion opposée à celle des autres tout en restant poli et respectueux ? Écris un exemple de phrase modèle.",
        "challenge_1_he": "איך להביע דעה מנוגדת לזו של אחרים תוך שמירה על נימוס וכבוד? כתוב דוגמה למשפט מופת.",
        "challenge_2_fr": "Joue un mini-jeu de rôle en binôme où chacun défend poliment et calmement deux avis différents sur son plat ou jeu préféré.",
        "challenge_2_he": "שחק משחק תפקידים קטן בזוגות שבו כל אחד מגן בנימוס וברוגע על שתי דעות שונות לגבי המאכל או המשחק האהוב עליו."
    },
    {
        "num": 40, "theme": "Courage & audace", 
        "quote": "On grandit chaque fois qu'on ose sortir de sa zone de confort.", 
        "quote_he": "אנחנו גדלים בכל פעם שאנחנו מעזים לצאת מאזור הנוחות.",
        "challenge_1_fr": "Écris une action simple mais inhabituelle qui se situe juste à la limite de ta zone de confort (ex: aller parler à un nouvel élève, lire devant la classe).",
        "challenge_1_he": "כתוב פעולה פשוטה אך לא שגרתית שנמצאת ממש על גבול אזור הנוחות שלך (למשל: ללכת לדבר עם תלמיד חדש, לקרוא מול הכיתה).",
        "challenge_2_fr": "Fais un pas en dehors de ta place de classe, ferme les yeux et étire tes bras vers le ciel pour matérialiser cette sortie de zone.",
        "challenge_2_he": "עשה צעד מחוץ למקום שלך בכיתה, עצום עיניים ומתח את זרועותיך אל השמיים כדי להמחיש את היציאה מהאזור."
    },

    # Gratitude & positivité (41-45)
    {
        "num": 41, "theme": "Gratitude & positivité", 
        "quote": "Prendre le temps de dire merci change une relation.", 
        "quote_he": "להקדיש רגע להגיד תודה יכול לשנות קשר.",
        "challenge_1_fr": "Rédige une petite lettre ou un message de gratitude sincère pour remercier chaleureusement un de tes camarades ou ton enseignant.",
        "challenge_1_he": "כתוב מכתב קטן או הודעה של הכרת תודה כנה כדי להודות בחמימות לאחד מחבריך לכיתה או למורה שלך.",
        "challenge_2_fr": "Plie ton mot en forme d'origami ou d'avion en papier et va le donner à la personne pour égayer sa journée.",
        "challenge_2_he": "קפל את הפתק שלך לצורת אוריגמי או מטוס נייר ולך לתת אותו לאותו אדם כדי לשמח את יומו."
    },
    {
        "num": 42, "theme": "Gratitude & positivité", 
        "quote": "Chaque jour contient au moins une bonne raison de sourire.", 
        "quote_he": "בכל יום יש לפחות סיבה טובה אחת לחייך.",
        "challenge_1_fr": "Cherche bien et note trois petits moments agréables et positifs qui se sont déroulés aujourd'hui dans ta journée d'école.",
        "challenge_1_he": "חפש היטב ורשום שלושה רגעים נעימים וחיוביים שהתרחשו היום במהלך יומך בבית הספר.",
        "challenge_2_fr": "Partage ces trois bonnes raisons de sourire avec tes voisins de classe et écoute les leurs.",
        "challenge_2_he": "שתף את שלוש הסיבות הטובות הללו לחיוך עם השכנים שלך לכיתה והקשב לשלהם."
    },
    {
        "num": 43, "theme": "Gratitude & positivité", 
        "quote": "Voir le positif ne veut pas dire ignorer le difficile.", 
        "quote_he": "לראות את הצד החיובי לא אומר להתעלם מהקושי.",
        "challenge_1_fr": "Pense à une situation un peu désagréable de ta journée. Essaie de l'analyser pour y trouver un apprentissage ou un côté positif caché.",
        "challenge_1_he": "חשוב על סיטואציה קצת לא נעימה מהיום שלך. נסה לנתח אותה כדי למצוא בה למידה או נקודת אור חבויה.",
        "challenge_2_fr": "Dessine un nuage de pluie (pour le difficile) traversé par un grand soleil brillant (pour le positif retrouvé).",
        "challenge_2_he": "צייר ענן גשם (שמייצג את הקושי) שנחצה על ידי שמש גדולה ומאירה (שמייצגת את החיובי שנמצא)."
    },
    {
        "num": 44, "theme": "Gratitude & positivité", 
        "quote": "La gratitude rend ce que l'on a suffisant.", 
        "quote_he": "הכרת תודה הופכת את מה שיש לך למספיק.",
        "challenge_1_fr": "Écris pourquoi tu es reconnaissant(e) d'avoir accès à tes livres de classe, à ton déjeuner ou à tes camarades de jeu aujourd'hui.",
        "challenge_1_he": "כתוב מדוע אתה אסיר תודה על הגישה לספרי הלימוד שלך, לארוחת הצהריים או לחברים שלך למשחק היום.",
        "challenge_2_fr": "Dis un grand 'Merci !' silencieux dans ton cœur en pensant à ces privilèges précieux de ta journée.",
        "challenge_2_he": "אמור 'תודה!' גדולה ושקטה בלבך תוך כדי מחשבה על הזכויות היקרות הללו ביומך."
    },
    {
        "num": 45, "theme": "Gratitude & positivité", 
        "quote": "Remarquer les efforts des autres, c'est déjà un cadeau.", 
        "quote_he": "לשים לב למאמצים של אחרים זו כבר מתנה.",
        "challenge_1_fr": "Quel effort discret as-tu remarqué aujourd'hui chez un camarade de classe, tes parents ou ton enseignant ? Écris-le pour lui rendre hommage.",
        "challenge_1_he": "שים לב למאמץ שקט שהבחנת בו היום אצל חבר לכיתה, ההורים שלך או המורה שלך? כתוב אותו כדי להביע הערכה.",
        "challenge_2_fr": "Va dire gentiment à cette personne : 'J'ai vu l'effort que tu as fait pour ... et je trouve ça super !'",
        "challenge_2_he": "לך להגיד בעדינות לאותו אדם: 'ראיתי את המאמץ שעשית כדי... ואני חושב שזה נהדר!'"
    },

    # Respect & écoute (46-50)
    {
        "num": 46, "theme": "Respect & écoute", 
        "quote": "Écouter vraiment, c'est offrir toute son attention.", 
        "quote_he": "להקשיב באמת זה לתת את כל תשומת הלב.",
        "challenge_1_fr": "Aujourd'hui, quand ton enseignant ou un camarade te parle, regarde-le avec attention sans te laisser distraire par tes affaires. Raconte comment s'est passée cette connexion.",
        "challenge_1_he": "היום, כאשר המורה או חבר מדברים אליך, הביט בהם בתשומת לב מבלי לתת לחפצים שלך להסיח את דעתך. תאר איך עבר החיבור הזה.",
        "challenge_2_fr": "Ferme les yeux pendant 10 secondes et concentre-toi sur le rythme de ta propre respiration pour affûter ton attention avant d'écouter.",
        "challenge_2_he": "עצום עיניים למשך 10 שניות והתרכז בקצב הנשימה שלך כדי לחדד את הקשב שלך לפני ההקשבה."
    },
    {
        "num": 47, "theme": "Respect & écoute", 
        "quote": "Le respect commence par laisser l'autre finir sa phrase.", 
        "quote_he": "כבוד מתחיל בכך שנותנים לאחר לסיים את המשפט שלו.",
        "challenge_1_fr": "Aujourd'hui, fais l'effort conscient de ne jamais couper la parole à personne. Raconte si cela t'a demandé de l'effort ou de la patience.",
        "challenge_1_he": "היום, עשה מאמץ מודע לא לקטוע את דבריו של אף אדם. ספר אם זה דרש ממך מאמץ או סבלנות.",
        "challenge_2_fr": "Fais un geste de verrouillage doux de tes lèvres avec tes doigts (comme une fermeture éclair imaginaire) lorsque tu as envie d'interrompre quelqu'un.",
        "challenge_2_he": "עשה תנועה עדינה של נעילת השפתיים שלך עם האצבעות (כמו רוכסן דמיוני) כאשר מתעורר בך החשק לקטוע מישהו."
    },
    {
        "num": 48, "theme": "Respect & écoute", 
        "quote": "On peut ne pas être d'accord et rester respectueux.", 
        "quote_he": "אפשר לא להסכים ובכל זאת להישאר מכבדים.",
        "challenge_1_fr": "Imagine que tu as un désaccord sur les règles d'un jeu dans la cour. Écris une phrase d'exemple respectueuse et amicale pour l'expliquer calmement.",
        "challenge_1_he": "דמיין שיש לך אי-הסכמה על חוקי משחק בחצר. כתוב משפט דוגמה מכבד וחברותי כדי להסביר זאת ברוגע.",
        "challenge_2_fr": "Joue cette scène calmement avec ton voisin en utilisant ta phrase respectueuse.",
        "challenge_2_he": "שחק את הסצנה הזו ברוגע עם השכן שלך תוך שימוש במשפט המכבד שלך."
    },
    {
        "num": 49, "theme": "Respect & écoute", 
        "quote": "Chaque avis mérite d'être entendu avant d'être discuté.", 
        "quote_he": "כל דעה ראויה להישמע לפני שדנים בה.",
        "challenge_1_fr": "Pourquoi est-il intéressant et enrichissant de connaître l'avis des autres même si tu penses détenir la meilleure opinion ? Rédige ton avis.",
        "challenge_1_he": "מדוע זה מעניין ומעשיר להכיר את דעתם של אחרים גם אם אתה חושב שדעתך היא הטובה ביותר? כתוב את חוות דעתך.",
        "challenge_2_fr": "Demande à ton voisin de table son avis sur un sujet léger (ex : le meilleur pouvoir magique) et écoute ses arguments avec respect.",
        "challenge_2_he": "שאל את השכן שלך לשולחן לדעתו בנושא קליל (למשל: כוח הקסם הכי טוב) והקשב לטיעוניו בכבוד."
    },
    {
        "num": 50, "theme": "Respect & écoute", 
        "quote": "Le silence, parfois, est la meilleure façon d'écouter.", 
        "quote_he": "לפעמים, השתיקה היא הדרך הכי טובה להקשיב.",
        "challenge_1_fr": "Ferme les yeux pendant 30 secondes complètes en classe ou dans ta chambre. Quels sons discrets ou bruits as-tu découverts grâce au silence ? Note-les.",
        "challenge_1_he": "עצום עיניים למשך 30 שניות שלמות בכיתה או בחדרך. אילו קולות שקטים או רעשים גילית בזכות השתיקה? רשום אותם.",
        "challenge_2_fr": "Faites l'expérience du silence collectif en classe pendant 1 minute complète sous la direction de l'enseignant.",
        "challenge_2_he": "חוו את חוויית השתיקה הקבוצתית בכיתה למשך דקה שלמה בהנחיית המורה."
    },

    # Créativité & imagination (51-55)
    {
        "num": 51, "theme": "Créativité & imagination", 
        "quote": "Il n'y a pas une seule bonne façon de résoudre un problème.", 
        "quote_he": "אין רק דרך אחת נכונה לפתור בעיה.",
        "challenge_1_fr": "Fais preuve d'imagination : trouve et écris trois utilisations complètement folles, amusantes et insolites pour un simple trombone ou un crayon à papier.",
        "challenge_1_he": "גלה דמיון: מצא וכתוב שלושה שימושים משוגעים, משעשעים ולא שגרתיים לחלוטין עבור אטב נייר פשוט או עיפרון.",
        "challenge_2_fr": "Présente tes trois idées créatives à ton groupe de travail et votez pour l'idée la plus loufoque de la table.",
        "challenge_2_he": "הצג את שלושת הרעיונות היצירתיים שלך לקבוצת העבודה שלך והצביעו עבור הרעיון המשוגע ביותר בשולחן."
    },
    {
        "num": 52, "theme": "Créativité & imagination", 
        "quote": "L'imagination transforme une feuille blanche en univers.", 
        "quote_he": "הדמיון הופך דף ריק ליקום שלם.",
        "challenge_1_fr": "Ferme les yeux et imagine une île lointaine et magique. Décris en deux phrases poétiques ce que l'on y trouve de surprenant.",
        "challenge_1_he": "עצום עיניים ודמיין אי רחוק וקסום. תאר בשני משפטים פיוטיים מה ניתן למצוא שם שמפתיע במיוחד.",
        "challenge_2_fr": "Dessine un croquis rapide de cette île mystérieuse dans un coin de ton cahier avec tes crayons de couleur.",
        "challenge_2_he": "צייר סקיצה מהירה של האי המסתורי הזה בפינת המחברת שלך בעזרת עפרונות הצבע שלך."
    },
    {
        "num": 53, "theme": "Créativité & imagination", 
        "quote": "Oser une idée originale, c'est déjà créer.", 
        "quote_he": "להעז עם רעיון מקורי זה כבר ליצור.",
        "challenge_1_fr": "Partage une idée créative un peu originale ou folle que tu as eue récemment, même si elle te semblait irréalisable à première vue.",
        "challenge_1_he": "שתף רעיון יצירתי קצת מקורי או משוגע שהיה לך לאחרונה, גם אם הוא נראה לך בלתי אפשרי במבט ראשון.",
        "challenge_2_fr": "Écris cette idée sur un petit morceau de papier coloré et colle-la sur le grand Arbre des Idées de la classe.",
        "challenge_2_he": "כתוב את הרעיון הזה על פיסת נייר צבעונית קטנה והדבק אותה על עץ הרעיונות הגדול של הכיתה."
    },
    {
        "num": 54, "theme": "Créativité & imagination", 
        "quote": "Se tromper en créant fait partie du processus.", 
        "quote_he": "לטעות תוך כדי יצירה זה חלק מהתהליך.",
        "challenge_1_fr": "Raconte un moment où tu as fait un dessin ou un projet manuel 'raté' que tu as finalement transformé en une autre création géniale.",
        "challenge_1_he": "ספר על רגע שבו עשית ציור או פרויקט יצירתי 'כושל' שלבסוף הפכת ליצירה נהדרת אחרת.",
        "challenge_2_fr": "Prends une feuille de brouillon, froisse-la légèrement pour faire des reliefs et sers-toi de ces plis pour imaginer un dessin en relief.",
        "challenge_2_he": "קח דף טיוטה, קמט אותו מעט כדי ליצור בליטות והשתמש בקמטים אלו כדי לדמיין ולצייר ציור תלת-ממדי."
    },
    {
        "num": 55, "theme": "Créativité & imagination", 
        "quote": "Chaque solution inattendue mérite d'être écoutée.", 
        "quote_he": "כל פתרון מפתיע ראוי להישמע.",
        "challenge_1_fr": "Quelle règle amusante ou idée insolite pourrais-tu inventer pour rendre le jeu habituel de la récréation encore plus collaboratif ?",
        "challenge_1_he": "איזה חוק משעשע או רעיון לא שגרתי היית יכול להמציא כדי להפוך את המשחק הרגיל בהפסקה לשיתופי עוד יותר?",
        "challenge_2_fr": "Propose cette nouvelle règle originale à tes amis lors de votre prochaine partie dans la cour de récréation.",
        "challenge_2_he": "הצע את החוק החדש והמקורי הזה לחברים שלך במהלך המשחק הבא שלכם בחצר בית הספר."
    },

    # Responsabilité & engagement (56-60)
    {
        "num": 56, "theme": "Responsabilité & engagement", 
        "quote": "Ce que tu fais aujourd'hui construit qui tu seras demain.", 
        "quote_he": "מה שאתה עושה היום בונה את מי שתהיה מחר.",
        "challenge_1_fr": "Quelle habitude responsable et citoyenne (ranger, lire, s'entraider, recycler) aimerais-tu faire grandir chez toi à partir d'aujourd'hui ?",
        "challenge_1_he": "איזה הרגל אחראי ואזרחי (לסדר, לקרוא, לעזור, למחזר) היית רוצה לפתח אצלך החל מהיום?",
        "challenge_2_fr": "Écris cet engagement responsable en lettres d'or dans ton journal d'éveil pour t'engager solennellement.",
        "challenge_2_he": "כתוב את ההתחייבות האחראית הזו באותיות מוזהבות ביומן התודעה שלך כדי להתחייב אליה באופן חגיגי."
    },
    {
        "num": 57, "theme": "Responsabilité & engagement", 
        "quote": "Tenir sa parole, c'est se respecter et respecter les autres.", 
        "quote_he": "לעמוד במילה שלך זה לכבד את עצמך ואת האחרים.",
        "challenge_1_fr": "Pourquoi est-il crucial pour toi de tenir tes promesses envers tes camarades de classe, tes parents ou tes enseignants ?",
        "challenge_1_he": "מדוע זה קריטי עבורך לעמוד בהבטחות שלך כלפי החברים שלך לכיתה, ההורים או המורים שלך?",
        "challenge_2_fr": "Pense à un engagement récent que tu as pris, et va voir la personne pour lui confirmer de vive voix que tu vas le faire.",
        "challenge_2_he": "חשוב על התחייבות שקיבלת על עצמך לאחרונה, ולך לפגוש את האדם כדי לאשר לו בעל פה שאתה אכן עומד לבצע אותה."
    },
    {
        "num": 58, "theme": "Responsabilité & engagement", 
        "quote": "Prendre une responsabilité, c'est montrer qu'on grandit.", 
        "quote_he": "לקחת אחריות זה להראות שאתה גדל.",
        "challenge_1_fr": "Quelle responsabilité concrète dans la vie de la classe (distribuer, soigner les plantes, ranger la bibliothèque...) aimerais-tu assurer ? Pourquoi ?",
        "challenge_1_he": "איזו אחריות מעשית בחיי הכיתה (חלוקת דפים, טיפול בצמחים, סידור הספרייה...) היית רוצה לקחת על עצמך? מדוע?",
        "challenge_2_fr": "Va proposer poliment ta candidature pour cette tâche ou responsabilité à ton enseignant.",
        "challenge_2_he": "לך להציע בנימוס את מועמדותך למשימה או לאחריות הזו למורה שלך."
    },
    {
        "num": 59, "theme": "Responsabilité & engagement", 
        "quote": "Un petit geste responsable peut inspirer tout un groupe.", 
        "quote_he": "מחווה אחראית קטנה יכולה לעורר השראה בקבוצה שלמה.",
        "challenge_1_fr": "Quel geste responsable et protecteur envers la nature ou la propreté de l'école as-tu accompli ou as-tu vu un camarade faire aujourd'hui ?",
        "challenge_1_he": "איזו מחווה אחראית ומגוננת כלפי הטבע או ניקיון בית הספר עשית או ראית חבר עושה היום?",
        "challenge_2_fr": "Ramasse un déchet qui traîne par terre dans la classe ou dans la cour de récréation et jette-le dans la poubelle de recyclage.",
        "challenge_2_he": "אסוף פריט פסולת זרוק על הרצפה בכיתה או בחצר והשלך אותו לפח המיחזור."
    },
    {
        "num": 60, "theme": "Responsabilité & engagement", 
        "quote": "S'engager, c'est choisir de faire sa part.", 
        "quote_he": "להתחייב זה לבחור לעשות את החלק שלך.",
        "challenge_1_fr": "Écris une action de solidarité collective que tu t'engages à faire pour que ta classe reste propre, solidaire et chaleureuse.",
        "challenge_1_he": "כתוב פעולה של סולידריות קבוצתית שאתה מתחייב לעשות כדי שהכיתה שלך תישאר נקייה, מגובשת וחמה.",
        "challenge_2_fr": "Fais un geste d'engagement physique en signant symboliquement le pacte d'engagement de la classe avec tes camarades de table.",
        "challenge_2_he": "עשה מחווה פיזית של התחייבות על ידי חתימה סמלית על אמנת ההתחייבות הכיתתית יחד עם חבריך לשולחן."
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
st.write(f"""<div class='main-title'>🌟 L'Éveil en Classe 🌟<br><span style='font-size: 2.1rem; opacity: 0.95;'>🌟 התעוררות בכיתה 🌟</span></div>""", unsafe_allow_html=True)
st.write("<div class='subtitle'>Messages Inspirants Bilingues & Choix de Défis Interactifs<br>מסרים מעוררי השראה דו-לשוניים ובחירת אתגרים אינטראקטיביים</div>", unsafe_allow_html=True)

# Demander le prénom au départ de la séance
if not st.session_state.user_name:
    st.info("👋 Bonjour ! Entre ton prénom pour commencer l'aventure de l'Éveil en Classe.\n\n👋 שלום! אנא הכנס את שמך כדי להתחיל את המסע.")
    cols_name = st.columns([3, 1])
    with cols_name[0]:
        name_input = st.text_input("Comment t'appelles-tu ?", placeholder="Ex: Lucas, Sofiane, Noam...", label_visibility="collapsed")
    with cols_name[1]:
        if st.button("Valider 🚀", use_container_width=True):
            if name_input.strip():
                st.session_state.user_name = name_input.strip()
                st.rerun()
            else:
                st.warning("N'oublie pas d'entrer ton prénom !\n\nאל תשכח להזין שם!")
    st.stop()

# Barre d'accueil personnalisée
st.write(f"### 🎈 Bienvenue dans ton espace d'Éveil, **{st.session_state.user_name}** !\n### 🎈 ברוך הבא, **{st.session_state.user_name}** !")

# --- COMPOSANT : AFFICHAGE DE LA CARTE ACTIVE EN FOCUS MODE ---
if st.session_state.current_card:
    card = st.session_state.current_card
    info = THEMES_INFO[card["theme"]]
    
    # Auto-reset flip states if it's a new card
    if st.session_state.get("last_card_num") != card["num"]:
        st.session_state.reveal_quote = False
        st.session_state.reveal_challenge = False
        st.session_state.last_card_num = card["num"]
        
    # Navigation et Sélecteur de Mode
    col_nav1, col_nav2 = st.columns([1, 1.5])
    with col_nav1:
        if st.button("⬅️ Retour au menu\n\nחזרה לתפריט", use_container_width=True):
            st.session_state.current_card = None
            if "wheel_theme" in st.session_state:
                del st.session_state["wheel_theme"]
            st.rerun()
            
    with col_nav2:
        learning_mode = st.radio(
            "Mode d'apprentissage :",
            ["🇫🇷 Français d'abord\nצרפתית תחילה", "🇮🇱 Hébreu d'abord\nעברית תחילה"],
            index=0,
            horizontal=True,
            label_visibility="collapsed"
        )
        
    if "last_learning_mode" not in st.session_state:
        st.session_state.last_learning_mode = learning_mode
    if st.session_state.last_learning_mode != learning_mode:
        st.session_state.reveal_quote = False
        st.session_state.reveal_challenge = False
        st.session_state.last_learning_mode = learning_mode

    # Structure visuelle de la carte en HTML/CSS
    # On décide quel texte afficher selon le mode d'apprentissage et si l'élève a révélé la carte
    if learning_mode == "🇫🇷 Français d'abord\nצרפתית תחילה":
        if not st.session_state.reveal_quote:
            quote_display_html = f'<div class="card-text">« {card["quote"]} »</div>'
        else:
            quote_display_html = clean_html(f'''
            <div class="card-text">« {card["quote"]} »</div>
            <div class="card-text-hebrew">"{card["quote_he"]}"</div>
            ''')
    else:  # Hébreu d'abord
        if not st.session_state.reveal_quote:
            quote_display_html = f'<div class="card-text-hebrew">"{card["quote_he"]}"</div>'
        else:
            quote_display_html = clean_html(f'''
            <div class="card-text">« {card["quote"]} »</div>
            <div class="card-text-hebrew">"{card["quote_he"]}"</div>
            ''')

    st.markdown(clean_html(f"""
    <div class="card-container" style="border: 4px solid {info['color']}; background-color: {info['bg_light']};">
        <span class="card-header-badge" style="background-color: {info['color']}; color: white;">
            {info['icon']} {card['theme']}
        </span>
        {quote_display_html}
        <div class="card-footer-info">
            Carte inspirante N°{card['num']} sur 60<br>קלף השראה מס' {card['num']} מתוך 60
        </div>
    </div>
    """), unsafe_allow_html=True)
    
    # Bouton interactif pour retourner le message de la carte
    if learning_mode == "🇫🇷 Français d'abord\nצרפתית תחילה":
        if not st.session_state.reveal_quote:
            if st.button("🔄 Retourner le message en Hébreu\n\nלגלות את המסר בעברית", use_container_width=True, type="secondary"):
                st.session_state.reveal_quote = True
                st.rerun()
        else:
            if st.button("🙈 Masquer l'Hébreu\n\nלהסתיר את המסר בעברית", use_container_width=True, type="secondary"):
                st.session_state.reveal_quote = False
                st.rerun()
    else:  # Hébreu d'abord
        if not st.session_state.reveal_quote:
            if st.button("🔄 Retourner le message en Français\n\nלגלות את המסר בצרפתית", use_container_width=True, type="secondary"):
                st.session_state.reveal_quote = True
                st.rerun()
        else:
            if st.button("🙈 Masquer le Français\n\nלהסתיר את המסר בצרפתית", use_container_width=True, type="secondary"):
                st.session_state.reveal_quote = False
                st.rerun()
                
    st.markdown("<hr style='margin: 25px 0; border: 1px dashed #BDC3C7;'>", unsafe_allow_html=True)
    
    # Saisie du défi au choix - Plusieurs défis bilingues au choix !
    st.markdown("<h3 style='text-align: center; font-family: Fredoka One, cursive;'>🎯 Choisis ton défi<br><span style='font-size: 1.5rem;'>בחר את האתגר שלך :</span></h3>", unsafe_allow_html=True)
    
    # Boutons ou Onglets locaux pour choisir le défi
    col_opt1, col_opt2 = st.columns(2)
    
    if "selected_defi_type" not in st.session_state:
        st.session_state.selected_defi_type = 1
        
    with col_opt1:
        if st.button("📝 Défi Écriture\n\nאתגר כתיבה ומחשבה", use_container_width=True, type="primary" if st.session_state.selected_defi_type == 1 else "secondary"):
            st.session_state.selected_defi_type = 1
            st.session_state.reveal_challenge = False # Reset challenge flip on change
            st.rerun()
            
    with col_opt2:
        if st.button("🏃 Défi Action\n\nאתגר פעולה ושיתוף", use_container_width=True, type="primary" if st.session_state.selected_defi_type == 2 else "secondary"):
            st.session_state.selected_defi_type = 2
            st.session_state.reveal_challenge = False # Reset challenge flip on change
            st.rerun()
            
    if st.session_state.selected_defi_type == 1:
        selected_challenge_fr = card["challenge_1_fr"]
        selected_challenge_he = card["challenge_1_he"]
        selected_type_fr = "📝 Défi Écriture & Réflexion"
        selected_type_he = "אתגר כתיבה ומחשבה"
        selected_type = "📝 Défi Écriture & Réflexion / אתגר כתיבה ומחשבה"
    else:
        selected_challenge_fr = card["challenge_2_fr"]
        selected_challenge_he = card["challenge_2_he"]
        selected_type_fr = "🏃 Défi Action & Partage"
        selected_type_he = "אתגר פעולה ושיתוף"
        selected_type = "🏃 Défi Action & Partage / אתגר פעולה ושיתוף"
        
    # Boîte d'affichage du défi sélectionné (bilingue adaptatif)
    if learning_mode == "🇫🇷 Français d'abord\nצרפתית תחילה":
        if not st.session_state.reveal_challenge:
            challenge_display_html = clean_html(f'''
            <h4 style="margin: 0 0 10px 0; color: {info['color']}; font-family: 'Fredoka One', cursive;">🔥 {selected_type_fr} :</h4>
            <p style="margin: 0; font-size: 1.15rem; color: #2C3E50; font-weight: bold;">{selected_challenge_fr}</p>
            ''')
        else:
            challenge_display_html = clean_html(f'''
            <h4 style="margin: 0 0 10px 0; color: {info['color']}; font-family: 'Fredoka One', cursive;">🔥 {selected_type} :</h4>
            <p style="margin: 0 0 12px 0; font-size: 1.15rem; color: #2C3E50; font-weight: bold;">{selected_challenge_fr}</p>
            <p style="margin: 0; font-size: 1.15rem; color: #34495E; font-weight: bold; direction: rtl; text-align: right;">{selected_challenge_he}</p>
            ''')
    else:  # Hébreu d'abord
        if not st.session_state.reveal_challenge:
            challenge_display_html = clean_html(f'''
            <h4 style="margin: 0 0 10px 0; color: {info['color']}; font-family: 'Fredoka One', cursive; direction: rtl; text-align: right;">🔥 {selected_type_he} :</h4>
            <p style="margin: 0; font-size: 1.15rem; color: #34495E; font-weight: bold; direction: rtl; text-align: right;">{selected_challenge_he}</p>
            ''')
        else:
            challenge_display_html = clean_html(f'''
            <h4 style="margin: 0 0 10px 0; color: {info['color']}; font-family: 'Fredoka One', cursive;">🔥 {selected_type} :</h4>
            <p style="margin: 0 0 12px 0; font-size: 1.15rem; color: #2C3E50; font-weight: bold;">{selected_challenge_fr}</p>
            <p style="margin: 0; font-size: 1.15rem; color: #34495E; font-weight: bold; direction: rtl; text-align: right;">{selected_challenge_he}</p>
            ''')

    st.markdown(clean_html(f"""
    <div class="challenge-box" style="border-left: 5px solid {info['color']};">
        {challenge_display_html}
    </div>
    """), unsafe_allow_html=True)
    
    # Bouton interactif pour retourner le défi
    if learning_mode == "🇫🇷 Français d'abord\nצרפתית תחילה":
        if not st.session_state.reveal_challenge:
            if st.button("🔍 Traduire la consigne en Hébreu\n\nלגלות את האתגר בעברית", use_container_width=True):
                st.session_state.reveal_challenge = True
                st.rerun()
        else:
            if st.button("🙈 Masquer la traduction du défi\n\nלהסתיר את האתגר בעברית", use_container_width=True):
                st.session_state.reveal_challenge = False
                st.rerun()
    else:  # Hébreu d'abord
        if not st.session_state.reveal_challenge:
            if st.button("🔍 Traduire la consigne en Français\n\nלגלות את האתגר בצרפתית", use_container_width=True):
                st.session_state.reveal_challenge = True
                st.rerun()
        else:
            if st.button("🙈 Masquer la traduction du défi\n\nלהסתיר את האתגר בצרפתית", use_container_width=True):
                st.session_state.reveal_challenge = False
                st.rerun()
                
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
    
    # Saisie de la réflexion bilingue
    ref_input = st.text_area("Écris ta réponse ici en français ou en hébreu :\nכתוב את תשובתך כאן בעברית או בצרפתית:", placeholder="Je pense que... / אני חושב ש...", height=120)
    
    if st.button("Valider mon Défi ! 🎉\n\nאשרו את האתגר שלי! 🎉", use_container_width=True):
        if len(ref_input.strip()) < 3:
            st.error("Ton défi est précieux ! Écris au moins un mot ou une petite phrase pour le valider.\n\nאנא כתוב לפחות מילה או משפט קצר כדי לאשר.")
        else:
            # Sauvegarde dans le journal bilingue
            new_entry = {
                "date": datetime.date.today().strftime("%d/%m/%Y"),
                "num": card["num"],
                "theme": card["theme"],
                "quote": card["quote"],
                "quote_he": card["quote_he"],
                "defi_type": selected_type,
                "defi_text_fr": selected_challenge_fr,
                "defi_text_he": selected_challenge_he,
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
                st.success(f"🏆 MAGNIFIQUE ! Tu as relevé le défi et débloqué le badge **{info['badge_name']}** !\n\n🏆 כל הכבוד! פתחת את התג!")
            else:
                st.balloons()
                st.success("🎉 Félicitations ! Ta réflexion a bien été ajoutée à ton Journal de l'Éveil !\n\n🎉 כל הכבוד! תשובתך נשמרה ביומן.")
            
            # Réinitialiser la carte pour encourager un autre tour si l'élève le souhaite
            st.session_state.current_card = None
            st.session_state.reveal_quote = False
            st.session_state.reveal_challenge = False
            if "wheel_theme" in st.session_state:
                del st.session_state["wheel_theme"]
            time.sleep(1)
            st.rerun()
            
    st.stop()
# Les Onglets de l'Application
tab_game, tab_wheel, tab_badges, tab_journal, tab_teacher = st.tabs([
    "🎲 Tirer une Carte\nהגרל קלף", 
    "🎡 La Roue de l'Éveil\nגלגל ההתעוררות",
    "🏆 Mes Badges\nהתגים שלי", 
    "📓 Mon Journal\nיומן אישי", 
    "🏫 Espace Enseignant\nמרחב מורה"
])

# --- ONGLETS 1 : TIRER UNE CARTE ---
with tab_game:
    st.markdown("### Choisis ton mode de tirage :\n### בחר את סוג ההגרלה :")
    
    cols_draw = st.columns(2)
    with cols_draw[0]:
        st.markdown("**🍀 Le hasard complet\n\nהגרלה אקראית**")
        if st.button("🎲 Tirer au sort une carte", use_container_width=True):
            st.session_state.current_card = random.choice(CARDS_DATA)
            st.rerun()
            
    with cols_draw[1]:
        st.markdown("**🎨 Choisir par Thème\n\nבחר לפי נושא**")
        theme_selected = st.selectbox("Choisis ton thème favori :", list(THEMES_INFO.keys()), label_visibility="collapsed")
        if st.button("🔍 Tirer une carte de ce thème", use_container_width=True):
            theme_cards = [c for c in CARDS_DATA if c["theme"] == theme_selected]
            st.session_state.current_card = random.choice(theme_cards)
            st.rerun()

# --- ONGLETS 2 : LA ROUE DE L'ÉVEIL ---
with tab_wheel:
    st.markdown("### 🎡 Lance la Roue Magique de l'Éveil !\n### סובב את גלגל ההתעוררות !")
    st.write("Fais tourner la roue virtuelle pour choisir ensemble le thème de discussion du jour en classe entière !\n\nסובבו את הגלגל כדי לבחור יחד את הנושא היומי לדיון כיתתי!")
    
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
            <p style="color: #7F8C8D; font-size: 1.2rem;">Le thème parfait pour aujourd'hui !<br>הנושא המושלם להיום!</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.success(f"✨ Le destin a parlé ! Nous allons travailler sur le thème **{selected_theme}** aujourd'hui.\n\n✨ הגורל קבע! היום נעבוד על נושא זה.")
        st.session_state.wheel_theme = selected_theme

    if "wheel_theme" in st.session_state:
        # Proposer directement de tirer une carte de ce thème
        if st.button(f"👉 Découvrir une carte du thème : {st.session_state.wheel_theme}\n\n👉 גלה קלף בנושא: {st.session_state.wheel_theme}", use_container_width=True):
            theme_cards = [c for c in CARDS_DATA if c["theme"] == st.session_state.wheel_theme]
            st.session_state.current_card = random.choice(theme_cards)
            del st.session_state["wheel_theme"]
            st.rerun()

# --- ONGLETS 3 : TABLEAU DES BADGES ---
with tab_badges:
    st.markdown("### 🏆 Ton Tableau de Chasse des Badges de l'Éveil\n### לוח התגים שלי")
    
    # Barre de progression
    unlocked_count = len(st.session_state.unlocked_badges)
    total_badges = len(THEMES_INFO)
    progress_ratio = unlocked_count / total_badges
    
    st.progress(progress_ratio)
    st.write(f"🎯 **Progression :** {unlocked_count} sur {total_badges} badges débloqués\n\n🎯 **התקדמות :** {unlocked_count} מתוך {total_badges} תגים פתוחים !")
    
    if unlocked_count == total_badges:
        st.success("👑 FANTASTIQUE ! Tu es devenu un(e) Maître de l'Éveil de la classe ! Tu as débloqué tous les badges !\n\n👑 מדהים! הפכת למאסטר התעוררות כיתתי!")

    # Grille des Badges
    st.write("---")
    badge_html = "<div class='badge-grid'>"
    for theme_name, info in THEMES_INFO.items():
        is_unlocked = theme_name in st.session_state.unlocked_badges
        if is_unlocked:
            badge_html += clean_html(f"""
            <div class="badge-card badge-active">
                <div class="badge-icon">{info['icon']}</div>
                <div class="badge-title" style="color: {info['color']};">{info['badge_name']}</div>
                <div style="font-size: 0.75rem; color: #7F8C8D; margin-top: 5px;">{info['badge_desc']}</div>
                <div style="font-size: 0.7rem; font-weight: bold; color: #2ECC71; margin-top: 5px;">Débloqué<br>פתוח !</div>
            </div>
            """)
        else:
            badge_html += clean_html(f"""
            <div class="badge-card" style="opacity: 0.5;">
                <div class="badge-icon" style="filter: grayscale(100%);">🔒</div>
                <div class="badge-title" style="color: #7F8C8D;">{theme_name}</div>
                <div style="font-size: 0.75rem; color: #BDC3C7; margin-top: 5px;">Fais un défi de ce thème pour l'ouvrir.<br>בצע אתגר בנושא זה כדי לפתוח.</div>
            </div>
            """)
    badge_html += "</div>"
    st.markdown(clean_html(badge_html), unsafe_allow_html=True)

# --- ONGLETS 4 : MON JOURNAL D'ÉVEIL ---
with tab_journal:
    st.markdown("### 📓 Ton Journal Personnel des Réflexions\n### היומן האישי שלי")
    st.write("Retrouve ici tout l'historique de tes pensées inspirantes et de tes actions de classe.\n\nמצא כאן את ההיסטוריה המלאה של המחשבות והפעולות שלך.")
    
    if not st.session_state.journal:
        st.warning("Ton journal est vide pour le moment. Tire une carte et relève ton premier défi pour l'inaugurer ! 📝\n\nהיומן שלך ריק כרגע. הגרל קלף ובצע אתגר ראשון!")
    else:
        # Affichage chronologique inversé (les plus récents en premier)
        for i, entry in enumerate(reversed(st.session_state.journal)):
            info = THEMES_INFO[entry["theme"]]
            st.markdown(clean_html(f"""
            <div style="background-color: #FFFFFF; border-radius: 15px; padding: 20px; border-left: 6px solid {info['color']}; margin-bottom: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.03);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <span style="font-weight: bold; color: {info['color']}; font-size: 1rem;">{info['icon']} {entry['theme']} - Carte N°{entry['num']}</span>
                    <span style="color: #BDC3C7; font-size: 0.85rem;">🗓️ Fait le {entry['date']}</span>
                </div>
                <p style="font-style: italic; color: #7F8C8D; border-left: 3px solid #ECF0F1; padding-left: 10px; margin: 10px 0;">"{entry['quote']}"</p>
                <p style="font-style: italic; color: #95A5A6; border-left: 3px solid #ECF0F1; padding-left: 10px; margin: 10px 0; direction: rtl; text-align: right;">"{entry['quote_he']}"</p>
                <div style="background-color: #F4F6F6; padding: 8px 12px; border-radius: 6px; margin: 10px 0;">
                    <p style="margin: 0; font-size: 0.85rem; color: #7F8C8D;"><b>Défi choisi / האתגר שנבחר:</b> {entry['defi_type']}</p>
                    <p style="margin: 4px 0 0 0; font-size: 0.95rem; color: #34495E;">{entry['defi_text_fr']}</p>
                    <p style="margin: 4px 0 0 0; font-size: 0.95rem; color: #7F8C8D; direction: rtl; text-align: right;">{entry['defi_text_he']}</p>
                </div>
                <div style="background-color: #F8F9F9; padding: 12px; border-radius: 8px; margin-top: 10px;">
                    <p style="margin: 0; font-weight: bold; font-size: 0.95rem; color: #2C3E50;">Ta réflexion / התשובה שלך :</p>
                    <p style="margin: 5px 0 0 0; color: #34495E; font-size: 1.05rem; white-space: pre-wrap;">{entry['reflection']}</p>
                </div>
            </div>
            """), unsafe_allow_html=True)
        
        # Option d'exportation du journal
        st.write("---")
        st.markdown("#### 📥 Exporter mon Journal / ייצוא היומן שלי")
        st.write("Tu peux télécharger toutes tes réponses dans un fichier pour l'envoyer à ton maître ou ta maîtresse, ou simplement l'imprimer !")
        
        journal_text = f"JOURNAL D'ÉVEIL DE / יומן אישי של : {st.session_state.user_name}\n"
        journal_text += f"Généré le / נוצר בתאריך : {datetime.date.today().strftime('%d/%m/%Y')}\n"
        journal_text += "="*50 + "\n\n"
        
        for entry in st.session_state.journal:
            journal_text += f"Date : {entry['date']}\n"
            journal_text += f"Thème : {entry['theme']} (Carte N°{entry['num']})\n"
            journal_text += f"Message inspirant : \"{entry['quote']}\" / \"{entry['quote_he']}\"\n"
            journal_text += f"Défi relevé : {entry['defi_type']}\n"
            journal_text += f"Consigne : {entry['defi_text_fr']} / {entry['defi_text_he']}\n"
            journal_text += f"Réflexion de {st.session_state.user_name} :\n{entry['reflection']}\n"
            journal_text += "-"*50 + "\n\n"
            
        st.download_button(
            label="💾 Télécharger mon journal (.txt)\n\nהורדת יומן",
            data=journal_text,
            file_name=f"journal_eveil_{st.session_state.user_name.lower()}.txt",
            mime="text/plain",
            use_container_width=True
        )

# --- ONGLETS 5 : ESPACE ENSEIGNANT ---
with tab_teacher:
    st.markdown("### 🏫 Espace Enseignant / מרחב מורה")
    
    # Sub-tabs for French and Hebrew instructions
    tab_teach_fr, tab_teach_he = st.tabs([
        "🇫🇷 Guide Enseignant (Français)",
        "🇮🇱 מדריך למורה (עברית)"
    ])
    
    with tab_teach_fr:
        st.markdown("### 🏫 Mode d'emploi et Usages Pédagogiques")
        st.write("Chers enseignants, voici comment tirer le meilleur parti de cette application interactive avec vos élèves :")
        
        st.markdown(clean_html("""
#### 1. Le Rituel du Matin (Collectif)
* **Comment faire ?** Projetez l'application au tableau (TBI / VPI) à l'arrivée des élèves.
* **Le jeu :** Allez sur l'onglet **Roue de l'Éveil**, faites tourner la roue magique devant la classe pour décider du thème. 
* **L'échange :** Tirez la carte associée et lisez-la ensemble. Laissez les élèves s'exprimer oralement sur le défi proposé pendant 5 minutes. C'est une excellente activité de transition pour démarrer la journée dans le calme et la positivité.

#### 2. Travail en Autonomie (Individuel sur Tablette/iPad)
* **Comment faire ?** Créez un QR code menant au lien de l'application et affichez-le en classe.
* **Le jeu :** Les élèves l'utilisent individuellement pendant les temps d'autonomie, après avoir fini un travail, ou lors d'ateliers d'Éducation Socioculturelle (EMC).
* **Le suivi :** À la fin de la semaine, demandez-leur de télécharger leur fichier journal (via l'onglet **Mon Journal d'Éveil**) et de vous le partager sur votre espace de travail habituel (ENT, Classroom, messagerie de classe) ou de l'imprimer pour enrichir leur portfolio de développement personnel.

#### 3. Débats Philosophiques et Ateliers de Langage
* **Comment faire ?** Utilisez les thèmes et citations comme inducteurs d'écriture ou de débats.
* **Exemple d'exercice :** Choisissez une carte difficile, par exemple le N°43 : *« Voir le positif ne veut pas dire ignorer le difficile »*. Demandez aux élèves d'écrire leur réponse à ce défi directement dans l'application, puis organisez un cercle de parole en classe pour confronter les idées.
"""), unsafe_allow_html=True)
        
        st.info("💡 **Conseil d'utilisation de la version en ligne :** Les données de cette application sont stockées localement dans le navigateur de l'appareil (Session State). Si l'élève ferme l'onglet, son journal se réinitialise. Pensez à lui rappeler d'exporter son journal à la fin d'une séance de travail si vous souhaitez l'évaluer !")
        
    with tab_teach_he:
        st.markdown(clean_html("""<div style="direction: rtl; text-align: right; font-family: sans-serif;">
    <h3 style="font-family: 'Fredoka One', cursive; color: #4A90E2; margin-top: 0;">🏫 מדריך למורה ושימושים פדגוגיים</h3>
    <p style="font-size: 1.1rem; color: #2C3E50; margin-bottom: 20px;">מורים יקרים, להלן דרכים להפיק את המרב מהאפליקציה האינטראקטיבית עם התלמידים שלכם:</p>
    
    <h4 style="color: #27AE60; margin-top: 25px;">1. ריטואל בוקר כיתתי (קבוצתי)</h4>
    <ul>
        <li><b>כיצד עושים זאת?</b> הקרינו את האפליקציה על הלוח (לוח חכם או מקרן) עם הגעת התלמידים לכיתה.</li>
        <li><b>המשחק:</b> היכנסו ללשונית "גלגל ההתעוררות" (La Roue de l'Éveil), סובבו את הגלגל הקסום מול הכיתה כדי לקבוע את הנושא היומי.</li>
        <li><b>השיח והשיתוף:</b> משכו את הקלף המתאים וקראו אותו יחד. אפשרו לתלמידים להתבטא בעל פה לגבי האתגר המוצע במשך 5 דקות. זוהי פעילות מעבר מצוינת להתחיל את היום ברוגע ובאווירה חיובית.</li>
    </ul>
    
    <h4 style="color: #E67E22; margin-top: 25px;">2. עבודה עצמאית (אישית על טאבלט/אייפד)</h4>
    <ul>
        <li><b>כיצד עושים זאת?</b> צרו קוד QR המוביל לקישור של האפליקציה שלכם והציגו אותו בכיתה.</li>
        <li><b>המשחק:</b> התלמידים משתמשים באפליקציה באופן אישי בזמני עבודה עצמאית, לאחר סיום משימה, או במהלך פעילויות חינוך חברתי.</li>
        <li><b>המעקב והמשך העבודה:</b> בסוף השבוע, בקשו מהם להוריד את קובץ היומן שלהם (דרך לשונית "יומן אישי" - Mon Journal) ולשתף אותו איתכם במרחב הלמידה הכיתתי הרגיל שלכם (מייל, קלאסרום, פורטל כיתתי) או להדפיס אותו כדי להעשיר את תיק העבודות (פורטפוליו) האישי שלהם.</li>
    </ul>
    
    <h4 style="color: #8E44AD; margin-top: 25px;">3. דיונים פילוסופיים וסדנאות שפה</h4>
    <ul>
        <li><b>כיצד עושים זאת?</b> השתמשו בנושאים ובציטוטים השונים כטריגרים לכתיבה יוצרת או לדיון פילוסופי קבוצתי.</li>
        <li><b>דוגמה לתרגיל:</b> בחרו קלף מורכב, למשל מס' 43: <i>"לראות את הצד החיובי לא אומר להתעלם מהקושי"</i>. בקשו מהתלמידים לכתוב את תשובתם לאתגר זה ישירות באפליקציה, ולאחר מכן ארגנו מעגל שיח בכיתה כדי להשוות ולשתף את הרעיונות של כולם.</li>
    </ul>
    
    <div style="background-color: #E8F8F5; border-right: 5px solid #2ECC71; border-radius: 8px; padding: 15px; margin-top: 30px;">
        <p style="margin: 0; color: #16A085; font-size: 1rem;">💡 <b>טיפ לשימוש באפליקציה המקוונת:</b> הנתונים באפליקציה זו נשמרים באופן זמני ומקומי בדפדפן המכשיר (Session State). אם התלמיד יסגור את הלשונית, היומן שלו יתאפס. זכרו להזכיר לו לייצא ולהוריד את היומן בסוף השיעור אם ברצונכם להעריך את עבודתו!</p>
    </div>
</div>"""), unsafe_allow_html=True)


# --- FOOTER DISCRET / חתימה דיסקרטית ---
st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
st.markdown("---")
st.markdown(clean_html("""
<div style="text-align: center; color: #BDC3C7; font-size: 0.85rem; margin-top: 10px; font-family: 'Quicksand', sans-serif;">
    Application créée par <b>Grace Sella</b> • Septembre 2026<br>
    <span style="direction: rtl; display: inline-block;">אפליקציה זו נוצרה על ידי <b>גרייס סלע</b> • ספטמבר 2026</span>
</div>
"""), unsafe_allow_html=True)
