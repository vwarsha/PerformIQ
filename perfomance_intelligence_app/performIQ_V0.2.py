import streamlit as st
import pandas as pd
import datetime as datetime
import os
import plotly.express as px

st.set_page_config(
    page_title="PerformIQ",
    page_icon="🏏",
    layout="centered"
)

st.title("PerformIQ — Athlete Performance Intelligence")
st.subheader("Session Input")

DATA_FILE = "data.csv"
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=[
        "Athlete name", "Sport", "Session", "Drill",
        "Execution", "Consistency", "Workload", "Date", "Performance index"
    ])

DRILL_OPTIONS = {
    "Cricket": [
        "Bowling Accuracy Drills",
        "Batting Footwork Drills",
        "Field Agility Drills",
        "Endurance Training",
        "None"
    ],
    "Running": [
        "Sprint Intervals",
        "Long-Distance Pace Training",
        "Hill Running",
        "Stride Length Drills",
        "None"
    ],
    "Football": [
        "Passing Drills",
        "Shooting Accuracy",
        "Defensive Positioning",
        "Stamina Circuits",
        "None"
    ],
    "Basketball": [
        "Dribbling Drills",
        "Free Throw Practice",
        "Defensive Footwork",
        "Conditioning Runs",
        "None"
    ],
    "Others": ["None"]
}

RECOMMENDATIONS = {
    "Cricket": {
        "Bowling Accuracy Drills": {
            "improving": [
                "Your bowling accuracy is trending upward — keep focusing on release point consistency.",
                "Try marking a target on the pitch and aiming for it in every delivery during practice.",
                "Add variation: after every 10 accurate deliveries, attempt one intentional variation ball."
            ],
            "declining": [
                "Accuracy drops often come from grip or run-up rhythm issues — film yourself and check.",
                "Go back to basics: slow down your run-up and rebuild muscle memory before adding pace.",
                "Work with a coach or trusted teammate to identify if it's a technical or fatigue issue."
            ],
            "stable": [
                "You're consistent but not growing — set a tighter target zone to push accuracy further.",
                "Challenge yourself: reduce your warm-up deliveries by two each session.",
                "Track which line/length you miss most. That's your focus area."
            ]
        },
        "Batting Footwork Drills": {
            "improving": [
                "Footwork is responding well — now link it to shot selection in your next net session.",
                "Practice the same footwork patterns against a bowling machine to build game-speed reactions.",
                "Strong foundation: add a mental trigger word before each delivery to stay disciplined."
            ],
            "declining": [
                "Footwork declines often come from fatigue or distraction — check your recovery between sessions.",
                "Go back to shadow batting: footwork without the ball to reset your muscle memory.",
                "Consider reducing session intensity and focusing on quality of movement over quantity."
            ],
            "stable": [
                "Footwork is steady — now challenge yourself against more varied deliveries.",
                "Set a specific goal: improve your movement to off-stump deliveries this week.",
                "Add reaction drills: have someone call 'front' or 'back' randomly to sharpen decisions."
            ]
        },
        "Field Agility Drills": {
            "improving": [
                "Agility gains are showing — push your cone drill timings by 5% this week.",
                "Add directional change under ball-tracking pressure to simulate real fielding scenarios.",
                "Your ground fielding will improve naturally as agility builds — keep going."
            ],
            "declining": [
                "Agility drops may signal muscle fatigue — check if you have back-to-back high intensity days.",
                "Slow down the drill speed and focus on clean technique before chasing faster times.",
                "Prioritise one rest day before your next agility session to allow recovery."
            ],
            "stable": [
                "Agility is consistent — add a competitive element by timing yourself and trying to beat it.",
                "Focus on your weaker side: most fielders have a preferred direction. Work the other.",
                "Film one agility drill per session to spot inefficiencies you can't feel in the moment."
            ]
        },
        "Endurance Training": {
            "improving": [
                "Endurance base is building — this will show in your late-innings performances.",
                "Gradually increase your distance or time by 10% each week to keep adapting.",
                "Pair endurance work with a protein-rich recovery meal within 45 minutes."
            ],
            "declining": [
                "Endurance decline could mean overtraining or poor sleep/nutrition — review both.",
                "Reduce intensity this week: walk-run intervals instead of sustained effort.",
                "Hydration is often overlooked — ensure you're drinking enough before and during sessions."
            ],
            "stable": [
                "Endurance is maintained — add one tempo run per week to break the plateau.",
                "Track your resting heart rate: as fitness improves, it should trend downward.",
                "Set a game-specific endurance target: e.g., bowl 10 overs at full intensity without drop-off."
            ]
        },
        "None": {
            "improving": [
                "Good session overall — maintain momentum by keeping sessions consistent in timing.",
                "Note what felt best today in your training journal while it's fresh.",
                "Consistency over intensity: showing up daily matters more than any single session."
            ],
            "declining": [
                "Step back and check the basics: sleep, nutrition, and recovery before diagnosing technique.",
                "One poor session doesn't define a trend — give it two more before making changes.",
                "Talk to your coach or a trusted analyst about what you noticed today."
            ],
            "stable": [
                "Stable is good — but growth requires a small push. Add one new challenge this week.",
                "Review your goals and check if your current training directly addresses them.",
                "Set a micro-goal for the next session: one specific thing to do better."
            ]
        }
    },
    "Running": {
        "Sprint Intervals": {
            "improving": [
                "Speed is responding — increase interval count by one this week while maintaining quality.",
                "Focus on start mechanics: most sprint gains come from the first three steps.",
                "Record your split times to track exactly where in the interval you're gaining."
            ],
            "declining": [
                "Sprint decline is often neurological fatigue — rest for 48 hours before the next session.",
                "Reduce intervals by two and focus on full recovery between each repetition.",
                "Check if you're doing too much volume — quality sprints beat quantity every time."
            ],
            "stable": [
                "Add resistance sprints (slight incline or band) to break the plateau.",
                "Focus on arm drive and breathing pattern — these are often the hidden limiters.",
                "Set a time target 2% faster than your current best for one interval per session."
            ]
        },
        "Long-Distance Pace Training": {
            "improving": [
                "Aerobic base is growing — your body is adapting well. Stay the course.",
                "Add one structured tempo run per week to complement your long-distance work.",
                "Focus on cadence: aim for 170–180 steps per minute for optimal efficiency."
            ],
            "declining": [
                "Distance fatigue builds slowly — check if you increased volume too quickly.",
                "Reduce this week's long run by 20% and focus on easy conversational pace.",
                "Nutrition during long runs matters — ensure you're fuelling properly."
            ],
            "stable": [
                "Introduce one fartlek session per week to build pace variation.",
                "Set a race target: having a goal event sharpens long-distance training focus.",
                "Track your pace per km — even 5 seconds per km improvement is significant over distance."
            ]
        },
        "Hill Running": {
            "improving": [
                "Hill strength is building — this will translate directly to flat speed. Keep at it.",
                "Add downhill running practice: controlled descent builds quad strength and confidence.",
                "Increase hill gradient or length by 10% this week."
            ],
            "declining": [
                "Hills are demanding — check if you're allowing full recovery between hill sessions.",
                "Reduce gradient and focus on technique: high knees, forward lean, short powerful strides.",
                "One hill session per week is enough at this stage — quality over frequency."
            ],
            "stable": [
                "Add a timed hill repeat: same hill, same effort, track if your time improves.",
                "Focus on the top: most athletes slow at the crest — push through it.",
                "Try a new hill route to give your brain and body a fresh challenge."
            ]
        },
        "Stride Length Drills": {
            "improving": [
                "Stride mechanics are improving — now integrate them into your regular runs.",
                "Add bounding drills: exaggerated stride practice builds neuromuscular patterns.",
                "Film yourself from the side to see your actual stride vs what you feel."
            ],
            "declining": [
                "Stride issues often come from tight hip flexors — add a 5-minute hip stretch routine.",
                "Slow down the drills: technique at slow speed first, then build pace.",
                "Check footstrike: landing too far ahead of your centre of mass kills stride efficiency."
            ],
            "stable": [
                "Add a strides session: 6 x 80m at 90% effort focusing purely on length and relaxation.",
                "Pair stride drills with video review to see what's actually happening.",
                "Set a specific target: gain 5cm of stride length by end of the month."
            ]
        },
        "None": {
            "improving": [
                "Great session — keep the momentum by staying consistent with timing.",
                "Log what felt good today: that information is valuable for future sessions.",
                "Consistency is your biggest asset right now — protect it."
            ],
            "declining": [
                "Check the fundamentals: sleep, hydration, and nutrition before adjusting training.",
                "One tough session isn't a trend — stay calm and show up tomorrow.",
                "Consider a lighter active recovery session before pushing hard again."
            ],
            "stable": [
                "Set one specific goal for your next session to add direction.",
                "Review your weekly volume — sometimes stable means you need more, sometimes less.",
                "Talk to a coach about where to introduce variety."
            ]
        }
    }
}

def get_recommendation(sport, drill, trend):
    """Get sport and drill specific recommendation."""
    sport_recs = RECOMMENDATIONS.get(sport, {})
    drill_recs = sport_recs.get(drill, sport_recs.get("None", {}))
    
    if not drill_recs:
        # Generic fallback
        if trend == "improving":
            return ["Keep it up! Maintain your current routine and focus on consistency."]
        elif trend == "declining":
            return ["Review your training intensity, recovery and technique. Consider a rest day."]
        else:
            return ["Stable progress. Set a specific goal to push improvement further."]
    
    return drill_recs.get(trend, drill_recs.get("stable", ["Keep working consistently."]))


def calculate_streaks(athlete_df):
    """Calculate current improving streak and days since last session."""
    if len(athlete_df) < 1:
        return 0, 0

    df_copy = athlete_df.copy()
    df_copy["Date"] = pd.to_datetime(df_copy["Date"])
    df_copy = df_copy.sort_values("Date").reset_index(drop=True)

    # Days since last session
    last_session = df_copy.iloc[-1]["Date"]
    today = pd.Timestamp.now()
    days_missed = (today - last_session).days

    # Improving streak: consecutive sessions where performance index went up
    streak = 0
    for i in range(len(df_copy) - 1, 0, -1):
        if df_copy.iloc[i]["Performance index"] > df_copy.iloc[i - 1]["Performance index"]:
            streak += 1
        else:
            break

    return streak, days_missed

def display_streak(streak, days_missed):
    """Display streak information with appropriate messaging."""
    st.subheader("🔥 Streak Tracker")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            label="Improving Streak",
            value=f"{streak} session{'s' if streak != 1 else ''}",
            help="Consecutive sessions where your performance index improved"
        )
    
    with col2:
        st.metric(
            label="Days Since Last Session",
            value=f"{days_missed} day{'s' if days_missed != 1 else ''}",
            help="Days elapsed since your most recent logged session"
        )

    if streak >= 5:
        st.success(f"🚀 **{streak}-session improving streak!** You're in a peak performance phase. Protect it.")
    elif streak >= 3:
        st.success(f"⚡ **{streak} sessions improving in a row.** Momentum is building — don't break the chain.")
    elif streak >= 1:
        st.info(f"📈 **{streak} session improving streak.** Good direction — keep it going.")
    else:
        st.warning("📊 No current improving streak. Focus on quality over the next 2–3 sessions.")

    if days_missed == 0:
        st.info("✅ Trained today — excellent commitment.")
    elif days_missed == 1:
        st.info("✅ Trained yesterday — on track.")
    elif days_missed <= 3:
        st.warning(f"⚠️ {days_missed} days since last session — don't let the gap widen.")
    else:
        st.error(f"🔴 {days_missed} days since last session — time to get back on track.")


name = st.text_input("Athlete Name")
sport = st.selectbox("Select Sport", list(DRILL_OPTIONS.keys()))
drill_options = DRILL_OPTIONS[sport]

with st.form(key="session_form"):
    session = st.selectbox("Session Type", ["Training", "Conditioning", "Match"])
    drill = st.selectbox("Select Drill (Optional)", drill_options)
    date = st.date_input("Session Date")

    execution = st.slider("Execution Quality (1–10)", 1, 10)
    consistency = st.slider("Consistency (1–10)", 1, 10)
    workload = st.slider("Workload Sustainability (1–10)", 1, 10)

    submitted = st.form_submit_button("Submit Session")

if submitted:
    if not name:
        st.error("Please enter the athlete name!")
    else:
        performance_index = (0.4 * execution) + (0.4 * consistency) + (0.2 * workload)

        new_row = pd.DataFrame([{
            "Athlete name": name,
            "Sport": sport,
            "Session": session,
            "Drill": drill,
            "Execution": execution,
            "Consistency": consistency,
            "Workload": workload,
            "Date": date,
            "Performance index": performance_index
        }])

        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("Session saved successfully!")

        # ── Performance Score ──
        st.subheader("Performance Evaluation")
        st.metric(label="Overall Session Score", value=round(performance_index, 2))

        if performance_index >= 7.5:
            st.write("Status: Athlete Progressing Well ✅")
        elif performance_index <= 5.5:
            st.write("Status: Intervention Needed ⚠️")
        else:
            st.write("Status: Holding Level 📊")

        st.divider()

        # ── Athlete specific data ──
        df["Date"] = pd.to_datetime(df["Date"]).dt.date
        athlete_df = df[df["Athlete name"] == name].sort_values("Date")

        # ── Performance Trend Chart ──
        st.subheader("Performance Trend Over Time")
        fig = px.line(
            athlete_df, x="Date", y="Performance index",
            title="Performance Trend", markers=True,
            color_discrete_sequence=["#00b4d8"]
        )
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig)

        st.divider()

        # ── Trend Summary ──
        if len(athlete_df) >= 2:
            pre_score = athlete_df.iloc[:-1]["Performance index"]
            avg_pre = pre_score.mean()
            today_score = athlete_df.iloc[-1]["Performance index"]
            change = ((today_score - avg_pre) / avg_pre) * 100

            st.subheader("Trend Summary")
            col1, col2, col3 = st.columns(3)
            col1.metric("Previous Average", f"{avg_pre:.2f}")
            col2.metric("Today's Score", f"{today_score:.2f}")
            col3.metric("Change", f"{change:+.1f}%")

            if change >= 3:
                st.success("**IMPROVING** 📈")
                trend = "improving"
            elif change <= -3:
                st.error("**DECLINE** 📉")
                trend = "declining"
            else:
                st.warning("**STABLE** ➡️")
                trend = "stable"
        else:
            trend = "stable"
            st.write("Not enough data for trend analysis (need at least 2 sessions).")

        st.divider()

        # ── STREAK TRACKER ──
        streak, days_missed = calculate_streaks(athlete_df)
        display_streak(streak, days_missed)

        st.divider()

        # ── SPORT + DRILL SPECIFIC RECOMMENDATIONS ──
        st.subheader(f"Recommendations — {sport} / {drill}")
        recs = get_recommendation(sport, drill, trend)

        for i, rec in enumerate(recs, 1):
            st.write(f"**{i}.** {rec}")

        st.divider()

        # ── Session History ──
        st.subheader("Session History")
        st.dataframe(df)
