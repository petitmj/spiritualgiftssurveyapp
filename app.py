import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from datetime import datetime
import io

# Page configuration
st.set_page_config(page_title="Spiritual Gifts Survey", page_icon="✨", layout="wide")

# Initialize session state
if 'responses' not in st.session_state:
    st.session_state.responses = {}
if 'page' not in st.session_state:
    st.session_state.page = 'intro'

# Survey questions
questions = [
    "I have the ability to organize ideas, resources, time, and people effectively.",
    "I am willing to study and prepare for the task of teaching.",
    "I am able to relate the truths of God to specific situations.",
    "I have a God-given ability to help others grow in their faith.",
    "I possess a special ability to communicate the truth of salvation.",
    "I have the ability to make critical decisions when necessary.",
    "I am sensitive to the hurts of people.",
    "I experience joy in meeting needs through sharing possessions.",
    "I enjoy studying.",
    "I have delivered God's message of warning and judgment.",
    "I am able to sense the true motivation of persons and movements.",
    "I have a special ability to trust God in difficult situations.",
    "I have a strong desire to contribute to the establishment of new churches.",
    "I take action to meet physical and practical needs rather than merely talking about or planning to help.",
    "I enjoy entertaining guests in my home.",
    "I can adapt my guidance to fit the maturity of those working with me.",
    "I can delegate and assign meaningful work.",
    "I have an ability and desire to teach.",
    "I am usually able to analyze a situation correctly.",
    "I have a natural tendency to encourage others.",
    "I am willing to take the initiative in helping other Christians grow in their faith.",
    "I have an acute awareness of the emotions of other people, such as loneliness, pain, fear, and anger.",
    "I am a cheerful giver.",
    "I spend lots of time reading books and digging into facts.",
    "I feel that I have a message from God to deliver to others.",
    "I can recognize when a person is genuine/honest.",
    "I am a person of vision. I am able to communicate vision in such a way that others commit to making the vision a reality.",
    "I am willing to yield to God's will rather than question and waver.",
    "I would like to be more active in getting the gospel to people in other lands.",
    "It makes me happy to do things for people in need.",
    "I am successful in getting a group to do its work joyfully.",
    "I am able to make strangers feel at ease.",
    "I have the ability to plan learning and teaching approaches.",
    "I can identify those who need encouragement.",
    "I have trained Christians to be more obedient disciples of Christ.",
    "I am willing to do whatever it takes to see others come to Christ.",
    "I am attracted to people who are hurting.",
    "I am a generous giver.",
    "I am able to discover new truths.",
    "I have spiritual insights from Scripture concerning issues and people that compel me to speak out.",
    "I can sense when a person is acting in accord with God's will.",
    "I can trust in God even when things look dark.",
    "I can determine where God wants a group to go and help it get there.",
    "I have a strong desire to take the gospel to places where it has never been heard.",
    "I enjoy reaching out to new people in my church and community.",
    "I am sensitive to the needs of people.",
    "I have been able to make effective and efficient plans for accomplishing the goals of a group.",
    "I often am consulted when fellow Christians are struggling to make difficult decisions.",
    "I think about how I can comfort and encourage others in my congregation.",
    "I am able to give spiritual direction to others.",
    "I am able to present the gospel to lost persons in such a way that they accept the Lord and His salvation.",
    "I possess an unusual capacity to understand the feelings of those in distress.",
    "I have a strong sense of stewardship based on the recognition that God owns all things.",
    "I have delivered to other persons messages that have come directly from God.",
    "I can sense when a person is acting under God's leadership.",
    "I try to be in God's will continually and be available for His use.",
    "I feel that I should take the gospel to people who have different beliefs from me.",
    "I have an acute awareness of the physical needs of others.",
    "I am skilled in setting forth positive and precise steps of action.",
    "I like to meet visitors at church and make them feel welcome.",
    "I explain Scripture in such a way that others understand it.",
    "I can usually see spiritual solutions to problems.",
    "I welcome opportunities to help people who need comfort, consolation, encouragement, and counseling.",
    "I feel at ease in sharing Christ with nonbelievers.",
    "I can influence others to perform to their highest God-given potential.",
    "I recognize the signs of stress and distress in others.",
    "I desire to give generously and unpretentiously to worthwhile projects and ministries.",
    "I can organize facts into meaningful relationships.",
    "God gives me messages to deliver to His people.",
    "I am able to sense whether people are being honest when they tell of their religious experiences.",
    "I enjoy presenting the gospel to persons of other cultures and backgrounds.",
    "I enjoy doing little things that help people.",
    "I can give a clear, uncomplicated presentation.",
    "I have been able to apply biblical truth to the specific needs of my church.",
    "God has used me to encourage others to live Christlike lives.",
    "I have sensed the need to help other people become more effective in their ministries.",
    "I like to talk about Jesus to those who do not know Him.",
    "I have the ability to make strangers feel comfortable in my home.",
    "I have a wide range of study resources and know how to secure information.",
    "I feel assured that a situation will change for the glory of God even when the situation seems impossible.",
    "I feel strongly that my prayers for a sick person bring recovery for that person.",
    "Making music, singing or dancing always lifts my spirit.",
    "Sometimes when I pray, it seems as if the Spirit steps in and prays in words I cannot understand.",
    "When I pray for the sick, either they or I feel sensations of tingling or warmth.",
    "Singing, dancing to, or playing songs of praise to God for pure enjoyment is personally satisfying.",
    "I can speak to God in a language I have never learned.",
    "I enjoy praying for sick people because I know that many of them will be healed as a result.",
    "People have said they see the love of Jesus on my face when I sing, dance, or play music.",
    "Praying in tongues has been meaningful to me in my personal prayer life.",
    "Sometimes I have a strong sense that God wants to heal someone through my prayers or words.",
    "People have told me they were moved spiritually by my singing, dancing, or playing music.",
    "When I give a public message in tongues, I expect it to be interpreted.",
    "I have prayed for others and physical healing has actually happened.",
    "I enjoy using my musical talents to make music that glorifies God and benefit people.",
    "When I speak in tongues, I believe it is edifying to the group I am with."
]

# Gift mappings (question numbers are 1-indexed in original, but 0-indexed in our list)
gift_mappings = {
    "Leadership": [6, 16, 27, 43, 65],
    "Administration": [1, 17, 31, 47, 59],
    "Teaching": [2, 18, 33, 61, 73],
    "Knowledge": [9, 24, 39, 68, 79],
    "Wisdom": [3, 19, 48, 62, 74],
    "Prophecy": [10, 25, 40, 54, 69],
    "Discernment": [11, 26, 41, 55, 70],
    "Healing": [81, 84, 87, 90, 93],
    "Music": [82, 85, 88, 91, 94],
    "Tongues": [83, 86, 89, 92, 95],
    "Counseling": [20, 34, 49, 63, 75],
    "Shepherding": [4, 21, 35, 50, 76],
    "Faith": [12, 28, 42, 56, 80],
    "Evangelism": [5, 36, 51, 64, 77],
    "Apostleship": [13, 29, 44, 57, 71],
    "Service/Helps": [14, 30, 46, 58, 72],
    "Mercy": [7, 22, 37, 52, 66],
    "Giving": [8, 23, 38, 53, 67],
    "Hospitality": [15, 32, 45, 60, 78]
}

# Gift definitions
gift_definitions = {
    "Leadership": "The divine enablement to cast vision, motivate, and direct people to harmoniously accomplish the purposes of God.",
    "Administration": "The divine enablement to understand what makes an organization function and the special ability to plan and execute procedures that accomplish the goals of the ministry.",
    "Teaching": "The divine enablement to understand, clearly explain and apply the word of God causing greater Christlikeness in the lives of listeners.",
    "Knowledge": "The divine enablement to bring truth to the body through a revelation or Biblical insight.",
    "Wisdom": "The ability to apply knowledge to life in such a way as to make spiritual truths quite relevant and practical in proper decision making.",
    "Prophecy": "The divine enablement to reveal truth and proclaim it in a timely and relevant manner for understanding, correction, repentance, or edification.",
    "Discernment": "The divine enablement to distinguish between truth and error, to discern the spirits, differentiating between good and evil, right and wrong.",
    "Healing": "The divine enablement to be God's means for restoring people to wholeness.",
    "Music": "The special gift to praise God through music in such a way as to enhance the worship experience of other believers.",
    "Tongues": "The special ability to speak prayer or praise in a language not previously learned or to communicate a message from God to His people.",
    "Counseling": "The ability to help others reach their full potential by means of encouraging, challenging, comforting, and guiding.",
    "Shepherding": "The divine enablement to nurture, care for, and guide people toward on-going spiritual maturity and becoming like Christ.",
    "Faith": "The divine enablement to act on God's promises with confidence and unwavering belief in God's ability to fulfill his purposes.",
    "Evangelism": "The divine enablement to effectively communicate the gospel to unbelievers so they respond in faith and move toward discipleship.",
    "Apostleship": "The divine ability to start and oversee the development of new churches or ministry structures.",
    "Service/Helps": "The divine enablement to accomplish practical and necessary tasks which free-up, support, and meet the needs of others.",
    "Mercy": "The divine enablement to cheerfully and practically help those who are suffering or are in need by putting compassion into action.",
    "Giving": "The divine enablement to contribute money and resources to the work of the Lord with cheerfulness and liberality.",
    "Hospitality": "The divine enablement to care for people by providing fellowship, food, and shelter."
}

def generate_pdf_report():
    """Generate PDF report of spiritual gifts results"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1  # Center
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        textColor=colors.darkblue
    )
    
    content = []
    
    # Title
    content.append(Paragraph("Spiritual Gifts Survey Results", title_style))
    content.append(Spacer(1, 20))
    
    # Date
    content.append(Paragraph(f"Generated on: {datetime.now().strftime('%B %d, %Y')}", styles['Normal']))
    content.append(Spacer(1, 20))
    
    # Calculate scores
    scores = calculate_scores()
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    # Top 3 gifts
    content.append(Paragraph("Your Top 3 Spiritual Gifts", heading_style))
    content.append(Spacer(1, 12))
    
    for idx, (gift, score) in enumerate(sorted_scores[:3]):
        content.append(Paragraph(f"<b>{idx + 1}. {gift}</b> - Score: {score}/25", styles['Normal']))
        content.append(Paragraph(gift_definitions[gift], styles['Normal']))
        content.append(Spacer(1, 12))
    
    content.append(PageBreak())
    
    # All scores table
    content.append(Paragraph("Complete Gift Scores", heading_style))
    content.append(Spacer(1, 12))
    
    # Create table data
    table_data = [['Spiritual Gift', 'Score', 'Percentage']]
    for gift, score in sorted_scores:
        percentage = (score / 25 * 100)
        table_data.append([gift, f"{score}/25", f"{percentage:.1f}%"])
    
    # Create table
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    content.append(table)
    content.append(Spacer(1, 20))
    
    # Detailed descriptions
    content.append(Paragraph("Gift Descriptions", heading_style))
    content.append(Spacer(1, 12))
    
    for gift, score in sorted_scores:
        content.append(Paragraph(f"<b>{gift} (Score: {score}/25)</b>", styles['Normal']))
        content.append(Paragraph(gift_definitions[gift], styles['Normal']))
        content.append(Spacer(1, 12))
    
    # Build PDF
    doc.build(content)
    buffer.seek(0)
    return buffer

def calculate_scores():
    """Calculate scores for each spiritual gift"""
    scores = {}
    for gift, items in gift_mappings.items():
        # Convert 1-indexed to 0-indexed
        score = sum([st.session_state.responses.get(i, 0) for i in items])
        scores[gift] = score
    return scores

def intro_page():
    """Display introduction page"""
    st.title("✨ Spiritual Gifts Survey")
    
    st.markdown("""
    ### Welcome!
    
    This survey is designed to help you discover your spiritual gifts. 
    
    **Important Notes:**
    - This is not a test, so there are no wrong answers
    - If you've been a Christian for at least a few years, base your responses on personal experiences
    - If you're a new Christian, respond based on the desires of your heart
    - Answer honestly and don't overthink each question
    - This survey consists of 95 statements
    
    **Response Scale:**
    - **5** - Highly characteristic of me/definitely true for me
    - **4** - Most of the time this would describe me/be true for me
    - **3** - Frequently characteristic of me/true for me (about 50%)
    - **2** - Occasionally characteristic of me/true for me (about 25%)
    - **1** - Not at all characteristic of me/definitely untrue for me
    
    Remember: This tool is meant as a starting point to discover how God has gifted you, 
    not as an absolute indicator. It should be used alongside prayer, community feedback, 
    and practical experience in ministry.
    """)
    
    if st.button("Begin Survey", type="primary", width='stretch'):
        st.session_state.page = 'survey'
        st.rerun()

def survey_page():
    """Display survey questions"""
    st.title("Spiritual Gifts Survey")
    
    # Progress bar
    total_questions = len(questions)
    answered = len([r for r in st.session_state.responses.values() if r > 0])
    progress = answered / total_questions
    st.progress(progress)
    st.write(f"Progress: {answered}/{total_questions} questions answered")
    
    # Display questions in groups of 10
    st.markdown("### Rate each statement from 1 (Not at all characteristic) to 5 (Highly characteristic)")
    
    for i, question in enumerate(questions, 1):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**{i}.** {question}")
        with col2:
            st.session_state.responses[i] = st.select_slider(
                f"Q{i}",
                options=[1, 2, 3, 4, 5],
                value=st.session_state.responses.get(i, 3),
                key=f"q_{i}",
                label_visibility="collapsed"
            )
        
        if i % 10 == 0:
            st.divider()
    
    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Introduction", width='stretch'):
            st.session_state.page = 'intro'
            st.rerun()
    with col2:
        if answered == total_questions:
            if st.button("View Results →", type="primary", width='stretch'):
                st.session_state.page = 'results'
                st.rerun()
        else:
            st.button(f"Complete all questions ({total_questions - answered} remaining)", disabled=True, width='stretch')

def results_page():
    """Display results"""
    st.title("📊 Your Spiritual Gifts Results")
    
    scores = calculate_scores()
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    # Top 3 gifts
    st.markdown("### Your Top 3 Spiritual Gifts")
    cols = st.columns(3)
    for idx, (gift, score) in enumerate(sorted_scores[:3]):
        with cols[idx]:
            st.metric(f"#{idx + 1} {gift}", f"{score}/25")
            st.write(gift_definitions[gift])
    
    st.divider()
    
    # All scores
    st.markdown("### All Gift Scores")
    
    # Create DataFrame for better display
    df = pd.DataFrame(sorted_scores, columns=['Spiritual Gift', 'Score'])
    df['Percentage'] = (df['Score'] / 25 * 100).round(1)
    
    # Display as chart
    st.bar_chart(df.set_index('Spiritual Gift')['Score'])
    
    # Display as table
    st.dataframe(df, width='stretch', hide_index=True)
    
    st.divider()
    
    # Detailed descriptions
    st.markdown("### Gift Descriptions")
    for gift, score in sorted_scores:
        with st.expander(f"{gift} (Score: {score}/25)"):
            st.write(gift_definitions[gift])
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("← Retake Survey", width='stretch'):
            st.session_state.responses = {}
            st.session_state.page = 'survey'
            st.rerun()
    with col2:
        if st.button("Start Over", width='stretch'):
            st.session_state.responses = {}
            st.session_state.page = 'intro'
            st.rerun()
    with col3:
        if st.button("📄 Download PDF", type="primary", width='stretch'):
            pdf_buffer = generate_pdf_report()
            st.download_button(
                label="Download Spiritual Gifts Results",
                data=pdf_buffer,
                file_name=f"spiritual_gifts_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf"
            )

# Main app logic
def main():
    # Sidebar
    with st.sidebar:
        st.markdown("## Navigation")
        if st.button("🏠 Introduction", width='stretch'):
            st.session_state.page = 'intro'
            st.rerun()
        if st.button("📝 Survey", width='stretch'):
            st.session_state.page = 'survey'
            st.rerun()
        if len(st.session_state.responses) == len(questions):
            if st.button("📊 Results", width='stretch'):
                st.session_state.page = 'results'
                st.rerun()
        
        st.divider()
        st.markdown("""
        ### About
        This survey helps identify your spiritual gifts based on biblical teaching 
        from 1 Corinthians 12-14, Romans 12, and Ephesians 4.
        
        Remember: Every Christian has at least one spiritual gift, and gifts 
        are meant to build up the body of Christ.
        """)
    
    # Display appropriate page
    if st.session_state.page == 'intro':
        intro_page()
    elif st.session_state.page == 'survey':
        survey_page()
    elif st.session_state.page == 'results':
        results_page()

if __name__ == "__main__":
    main()