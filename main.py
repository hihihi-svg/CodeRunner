"""
DSA Racing Simulator - Streamlit Version
Answer correctly to dodge obstacles in real-time!

Run with: streamlit run app.py
"""

import streamlit as st
import time
import random
from collections import deque
import heapq
import json

# ===========================
# DATA STRUCTURES
# ===========================

class LifeNode:
    """Linked list node for lives"""
    def __init__(self):
        self.next = None

class LivesLinkedList:
    """Dynamic life management"""
    def __init__(self, initial=3):
        self.head = None
        self.size = 0
        for _ in range(initial):
            self.add_life()
    
    def add_life(self):
        node = LifeNode()
        if not self.head:
            self.head = node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = node
        self.size += 1
    
    def remove_life(self):
        if self.head:
            self.head = self.head.next
            self.size -= 1
            return True
        return False
    
    def get_count(self):
        return self.size
    
    def has_lives(self):
        return self.size > 0


class QuestionQueue:
    """FIFO queue for questions"""
    def __init__(self):
        self.queue = deque()
    
    def enqueue(self, question):
        self.queue.append(question)
    
    def dequeue(self):
        return self.queue.popleft() if self.queue else None
    
    def size(self):
        return len(self.queue)


class ScoreStack:
    """LIFO stack for score history"""
    def __init__(self):
        self.stack = []
    
    def push(self, score):
        self.stack.append(score)
    
    def peek(self):
        return self.stack[-1] if self.stack else 0


class Leaderboard:
    """Min heap for high scores"""
    def __init__(self):
        self.heap = []
        self.high_score = 0
    
    def add_score(self, score):
        heapq.heappush(self.heap, -score)
        if score > self.high_score:
            self.high_score = score
            return True
        return False


# ===========================
# QUESTION MANAGER
# ===========================

class QuestionManager:
    """Manages DSA questions with HashMap"""
    def __init__(self):
        self.question_map = self._load_questions()
        self.question_queue = QuestionQueue()
        self.current_question = None
    
    def _load_questions(self):
        """HashMap of questions - Write actual code functions"""
        return {
            "arrays_very_easy": [
                {"q": "Write function to find max in array:\ndef find_max(arr):\n    # Your code (return statement only)", "a": "return max(arr)", "topic": "Arrays", "diff": "Very Easy"},
                {"q": "Write function to sum array:\ndef sum_array(arr):\n    # Your code (return statement only)", "a": "return sum(arr)", "topic": "Arrays", "diff": "Very Easy"},
                {"q": "Write function for array length:\ndef get_length(arr):\n    # Your code (return statement only)", "a": "return len(arr)", "topic": "Arrays", "diff": "Very Easy"},
            ],
            "arrays_easy": [
                {"q": "Write function to reverse array:\ndef reverse_array(arr):\n    # Your code (return statement only)", "a": "return arr[::-1]", "topic": "Arrays", "diff": "Easy"},
                {"q": "Write function to find second max:\ndef second_max(arr):\n    # Your code (return statement only)", "a": "return sorted(arr)[-2]", "topic": "Arrays", "diff": "Easy"},
                {"q": "Write function to count even numbers:\ndef count_evens(arr):\n    # Your code (return statement only)", "a": "return sum(1 for x in arr if x % 2 == 0)", "topic": "Arrays", "diff": "Easy"},
            ],
            "strings_very_easy": [
                {"q": "Write function to check palindrome:\ndef is_palindrome(s):\n    # Your code (return statement only)", "a": "return s == s[::-1]", "topic": "Strings", "diff": "Very Easy"},
                {"q": "Write function to get string length:\ndef str_length(s):\n    # Your code (return statement only)", "a": "return len(s)", "topic": "Strings", "diff": "Very Easy"},
            ],
            "strings_easy": [
                {"q": "Write function to reverse string:\ndef reverse_string(s):\n    # Your code (return statement only)", "a": "return s[::-1]", "topic": "Strings", "diff": "Easy"},
                {"q": "Write function to count vowels:\ndef count_vowels(s):\n    # Your code (return statement only)", "a": "return sum(1 for c in s.lower() if c in 'aeiou')", "topic": "Strings", "diff": "Easy"},
            ],
            "stacks_very_easy": [
                {"q": "Write function to implement stack push:\ndef push(stack, item):\n    # Your code (return modified stack)", "a": "return stack + [item]", "topic": "Stack", "diff": "Very Easy"},
                {"q": "Write function for stack pop:\ndef pop(stack):\n    # Your code (return stack[:-1])", "a": "return stack[:-1]", "topic": "Stack", "diff": "Very Easy"},
            ],
            "stacks_easy": [
                {"q": "Write function to check balanced parentheses:\ndef is_balanced(s):\n    # Your code (return True/False)", "a": "return s.count('(') == s.count(')')", "topic": "Stack", "diff": "Easy"},
                {"q": "Write function for queue dequeue:\ndef dequeue(queue):\n    # Your code (return queue[1:])", "a": "return queue[1:]", "topic": "Queue", "diff": "Easy"},
            ],
            "searching_very_easy": [
                {"q": "Write linear search function:\ndef linear_search(arr, target):\n    # Your code (return index or -1)", "a": "return arr.index(target) if target in arr else -1", "topic": "Search", "diff": "Very Easy"},
                {"q": "Write function to check if element exists:\ndef exists(arr, x):\n    # Your code (return True/False)", "a": "return x in arr", "topic": "Search", "diff": "Very Easy"},
            ],
            "searching_easy": [
                {"q": "Write binary search (assume sorted):\ndef binary_search(arr, target):\n    # Return index using bisect", "a": "import bisect; return bisect.bisect_left(arr, target)", "topic": "Search", "diff": "Easy"},
            ],
            "recursion_easy": [
                {"q": "Write recursive factorial:\ndef factorial(n):\n    # Your code (single line)", "a": "return 1 if n <= 1 else n * factorial(n-1)", "topic": "Recursion", "diff": "Easy"},
                {"q": "Write recursive fibonacci:\ndef fib(n):\n    # Your code (single line)", "a": "return n if n <= 1 else fib(n-1) + fib(n-2)", "topic": "Recursion", "diff": "Easy"},
            ],
            "sorting_easy": [
                {"q": "Write function to sort array:\ndef sort_array(arr):\n    # Your code (return statement)", "a": "return sorted(arr)", "topic": "Sorting", "diff": "Easy"},
                {"q": "Write function to sort descending:\ndef sort_desc(arr):\n    # Your code (return statement)", "a": "return sorted(arr, reverse=True)", "topic": "Sorting", "diff": "Easy"},
            ],
            "trees_hard": [
                {"q": "Write BFS traversal skeleton:\ndef bfs(root):\n    # What data structure? (queue/stack)", "a": "queue", "topic": "Trees", "diff": "Hard"},
                {"q": "Write DFS traversal skeleton:\ndef dfs(root):\n    # What data structure? (queue/stack)", "a": "stack", "topic": "Trees", "diff": "Hard"},
            ],
        }
    
    def prepare_questions(self, difficulty, mode):
        """Load questions into queue"""
        self.question_queue = QuestionQueue()
        available = []
        
        diff_map = {"Very Easy": "very_easy", "Easy": "easy", "Hard": "hard"}
        diff_key = diff_map.get(difficulty, "easy")
        
        if mode == "Mixed":
            for key, questions in self.question_map.items():
                if diff_key in key:
                    available.extend(questions)
        else:
            # Topic-wise
            matching = [k for k in self.question_map.keys() if diff_key in k]
            if matching:
                key = random.choice(matching)
                available = self.question_map[key]
        
        random.shuffle(available)
        for q in available[:15]:
            self.question_queue.enqueue(q)
    
    def get_next_question(self):
        """Dequeue next question"""
        self.current_question = self.question_queue.dequeue()
        return self.current_question
    
    def check_answer(self, user_answer):
        """Validate answer"""
        if not self.current_question:
            return False
        correct = str(self.current_question['a']).strip().lower().replace(" ", "")
        user = str(user_answer).strip().lower().replace(" ", "")
        return correct == user


# ===========================
# INITIALIZE SESSION STATE
# ===========================

def init_session_state():
    """Initialize game state"""
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.game_state = "menu"
        st.session_state.language = "Python"
        st.session_state.difficulty = "Easy"
        st.session_state.mode = "Mixed"
        
        # Game objects
        st.session_state.lives = None
        st.session_state.score = 0
        st.session_state.streak = 0
        st.session_state.questions_answered = 0
        st.session_state.correct_answers = 0
        st.session_state.distance = 0
        
        # Managers
        st.session_state.qm = QuestionManager()
        st.session_state.score_stack = ScoreStack()
        st.session_state.leaderboard = Leaderboard()
        
        # Obstacle system
        st.session_state.obstacle_approaching = False
        st.session_state.obstacle_distance = 100
        st.session_state.obstacle_lane = "center"
        st.session_state.car_lane = "center"
        st.session_state.obstacle_speed = 5
        
        # Timer
        st.session_state.question_start_time = None
        st.session_state.time_limit = 300
        
        # Feedback
        st.session_state.feedback = ""
        st.session_state.feedback_type = ""


def start_game():
    """Start new game"""
    st.session_state.game_state = "playing"
    st.session_state.lives = LivesLinkedList(3)
    st.session_state.score = 0
    st.session_state.streak = 0
    st.session_state.questions_answered = 0
    st.session_state.correct_answers = 0
    st.session_state.distance = 0
    
    # Prepare questions
    st.session_state.qm.prepare_questions(
        st.session_state.difficulty,
        st.session_state.mode
    )
    
    # Load first question
    next_question()
    spawn_obstacle()


def next_question():
    """Load next question"""
    question = st.session_state.qm.get_next_question()
    if question:
        st.session_state.question_start_time = time.time()
        st.session_state.time_limit = {"Very Easy": 300, "Easy": 600, "Hard": 1200}[st.session_state.difficulty]
        return True
    else:
        st.session_state.game_state = "game_over"
        return False


def spawn_obstacle():
    """Spawn new obstacle"""
    st.session_state.obstacle_approaching = True
    st.session_state.obstacle_distance = 100
    lanes = ["left", "center", "right"]
    st.session_state.obstacle_lane = random.choice(lanes)
    st.session_state.obstacle_speed = random.randint(3, 7)


def update_game():
    """Update game state"""
    if st.session_state.game_state != "playing":
        return
    
    # Move obstacle closer
    if st.session_state.obstacle_approaching:
        st.session_state.obstacle_distance -= st.session_state.obstacle_speed
        st.session_state.distance += st.session_state.obstacle_speed * 0.1
        
        # Check collision
        if st.session_state.obstacle_distance <= 0:
            if st.session_state.obstacle_lane == st.session_state.car_lane:
                # CRASH!
                st.session_state.lives.remove_life()
                st.session_state.feedback = "💥 CRASH! You didn't dodge in time!"
                st.session_state.feedback_type = "error"
                st.session_state.streak = 0
                
                if not st.session_state.lives.has_lives():
                    st.session_state.game_state = "game_over"
                    return
            
            # Spawn next obstacle
            spawn_obstacle()
            next_question()


def submit_answer(answer):
    """Process answer"""
    if not answer:
        return
    
    elapsed = time.time() - st.session_state.question_start_time
    is_correct = st.session_state.qm.check_answer(answer)
    
    st.session_state.questions_answered += 1
    
    if is_correct:
        # DODGE!
        # Move car to avoid obstacle
        lanes = ["left", "center", "right"]
        lanes.remove(st.session_state.obstacle_lane)
        st.session_state.car_lane = random.choice(lanes)
        
        # Calculate score
        time_bonus = 10 if elapsed < 30 else 5 if elapsed < 60 else 0
        points = 20 + time_bonus
        st.session_state.score += points
        st.session_state.correct_answers += 1
        st.session_state.streak += 1
        
        # Bonus life
        if st.session_state.streak % 3 == 0:
            st.session_state.lives.add_life()
            st.session_state.feedback = f"✅ CORRECT! Dodged obstacle! +{points} pts | ❤️ BONUS LIFE!"
        else:
            st.session_state.feedback = f"✅ CORRECT! Dodged obstacle! +{points} pts"
        
        st.session_state.feedback_type = "success"
        
        # Push to stack
        st.session_state.score_stack.push(st.session_state.score)
        
        # Fast forward obstacle
        st.session_state.obstacle_distance = -10
        
    else:
        # WRONG - stay in lane, will crash
        correct = st.session_state.qm.current_question['a']
        st.session_state.feedback = f"❌ WRONG! Answer: {correct} - Can't dodge!"
        st.session_state.feedback_type = "error"
        st.session_state.streak = 0


# ===========================
# UI COMPONENTS
# ===========================

def render_menu():
    """Main menu"""
    st.markdown("""
    <style>
    .big-title {
        font-size: 60px;
        font-weight: bold;
        text-align: center;
        color: #00ff88;
        margin-bottom: 10px;
    }
    .subtitle {
        font-size: 24px;
        text-align: center;
        color: #888;
        margin-bottom: 40px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="big-title">🏎️ DSA RACING SIMULATOR</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Write Code to Dodge Obstacles!</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### ⚙️ Game Settings")
        
        st.session_state.language = st.selectbox(
            "Programming Language",
            ["Python", "C", "C++"],
            index=0
        )
        
        st.session_state.difficulty = st.selectbox(
            "Difficulty Level",
            ["Very Easy", "Easy", "Hard"],
            index=1
        )
        
        st.session_state.mode = st.selectbox(
            "Question Mode",
            ["Mixed", "Topic-wise"],
            index=0
        )
        
        st.markdown("---")
        
        st.markdown("""
        ### 📖 How to Play
        
        🚗 **Your car is in the center lane**
        
        🚧 **Obstacles approach from ahead**
        
        ✅ **Write CORRECT CODE = Dodge to safety!**
        
        ❌ **Write WRONG CODE = Stay in lane → CRASH!**
        
        💥 **3 Lives total | Lose all = Game Over**
        
        🔥 **3-streak = Bonus Life**
        
        ⏱️ **Timer varies by difficulty**
        """)
        
        st.markdown("---")
        
        if st.session_state.leaderboard.high_score > 0:
            st.success(f"🏆 High Score: {st.session_state.leaderboard.high_score}")
        
        if st.button("🚀 START RACING", use_container_width=True, type="primary"):
            start_game()
            st.rerun()


def render_game():
    """Game screen"""
    update_game()
    
    # Stats header
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        lives_str = "❤️" * st.session_state.lives.get_count()
        st.markdown(f"### {lives_str}")
    
    with col2:
        st.metric("Score", st.session_state.score)
    
    with col3:
        st.metric("Streak", f"🔥 {st.session_state.streak}")
    
    with col4:
        st.metric("Distance", f"{int(st.session_state.distance)}m")
    
    with col5:
        if st.session_state.question_start_time:
            elapsed = time.time() - st.session_state.question_start_time
            remaining = max(0, st.session_state.time_limit - elapsed)
            mins = int(remaining // 60)
            secs = int(remaining % 60)
            st.metric("Timer", f"{mins:02d}:{secs:02d}")
    
    st.markdown("---")
    
    # Racing view
    st.markdown("### 🛣️ Racing Track")
    
    # Visual representation
    render_racing_track()
    
    st.markdown("---")
    
    # Question section
    if st.session_state.qm.current_question:
        q = st.session_state.qm.current_question
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"### 📝 Question {st.session_state.questions_answered + 1}")
        with col2:
            st.info(f"**{q['topic']}** - {q['diff']}")
        
        st.code(q['q'], language='python')
        
        # Answer input
        answer = st.text_area(
            "Your Code:",
            key=f"answer_{st.session_state.questions_answered}",
            placeholder="Write your return statement here...",
            height=100
        )
        
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            if st.button("🚀 SUBMIT", use_container_width=True, type="primary"):
                submit_answer(answer)
                st.rerun()
        
        # Feedback
        if st.session_state.feedback:
            if st.session_state.feedback_type == "success":
                st.success(st.session_state.feedback)
            else:
                st.error(st.session_state.feedback)
    
    # Pause button
    st.markdown("---")
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("⏸️ PAUSE", use_container_width=True):
            st.session_state.game_state = "menu"
            st.rerun()
    
    # Auto-refresh for obstacle movement
    time.sleep(0.1)
    st.rerun()


def render_racing_track():
    """Visual racing track with sleek cars"""
    obstacle_dist = st.session_state.obstacle_distance
    obstacle_lane_idx = {"left": 0, "center": 1, "right": 2}[st.session_state.obstacle_lane]
    car_lane_idx = {"left": 0, "center": 1, "right": 2}[st.session_state.car_lane]
    
    # Create track visualization
    track_html = f"""
    <style>
    .track-container {{
        background: linear-gradient(180deg, #87CEEB 0%, #4a4a4a 50%, #2d2d2d 100%);
        border-radius: 10px;
        padding: 20px;
        min-height: 500px;
        position: relative;
        overflow: hidden;
    }}
    .road {{
        background: linear-gradient(180deg, #2a2a2a 0%, #1a1a1a 100%);
        width: 100%;
        height: 100%;
        position: relative;
        border-radius: 5px;
        display: flex;
        justify-content: space-between;
        padding: 0 20px;
        box-shadow: inset 0 0 50px rgba(0,0,0,0.8);
    }}
    .lane {{
        width: 28%;
        position: relative;
        border-left: 3px dashed #FFD700;
        border-right: 3px dashed #FFD700;
        min-height: 450px;
    }}
    .obstacle {{
        font-size: 40px;
        position: absolute;
        top: {max(0, 100 - obstacle_dist)}%;
        left: 50%;
        transform: translateX(-50%);
        animation: pulse 0.5s infinite;
        filter: drop-shadow(0 0 10px rgba(255,0,0,0.5));
    }}
    .car {{
        position: absolute;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        width: 80px;
        height: 120px;
    }}
    .car-body {{
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, #ff0000 0%, #cc0000 50%, #990000 100%);
        border-radius: 15px 15px 5px 5px;
        position: relative;
        box-shadow: 0 5px 20px rgba(255,0,0,0.4), inset 0 2px 10px rgba(255,255,255,0.2);
        animation: carFloat 2s ease-in-out infinite;
    }}
    .car-window {{
        width: 60%;
        height: 30%;
        background: linear-gradient(135deg, #1a1a2e 0%, #0f0f1e 100%);
        border-radius: 8px 8px 0 0;
        position: absolute;
        top: 10%;
        left: 20%;
        box-shadow: inset 0 2px 8px rgba(0,0,0,0.5);
    }}
    .car-stripe {{
        width: 20%;
        height: 80%;
        background: linear-gradient(180deg, #ffff00 0%, #ffaa00 100%);
        position: absolute;
        top: 10%;
        left: 40%;
        border-radius: 3px;
        box-shadow: 0 0 10px rgba(255,255,0,0.6);
    }}
    .car-wheel {{
        width: 15px;
        height: 15px;
        background: #1a1a1a;
        border-radius: 50%;
        position: absolute;
        border: 3px solid #333;
        box-shadow: inset 0 2px 5px rgba(0,0,0,0.8);
    }}
    .wheel-left {{
        left: 5px;
        bottom: 25px;
    }}
    .wheel-right {{
        right: 5px;
        bottom: 25px;
    }}
    .wheel-left-front {{
        left: 5px;
        bottom: 60px;
    }}
    .wheel-right-front {{
        right: 5px;
        bottom: 60px;
    }}
    .car-glow {{
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 100%;
        height: 30px;
        background: radial-gradient(ellipse at center, rgba(255,0,0,0.4) 0%, transparent 70%);
        filter: blur(10px);
    }}
    @keyframes pulse {{
        0%, 100% {{ transform: translateX(-50%) scale(1); }}
        50% {{ transform: translateX(-50%) scale(1.1); }}
    }}
    @keyframes carFloat {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-3px); }}
    }}
    .distance-marker {{
        position: absolute;
        right: 10px;
        top: 10px;
        background: rgba(0,0,0,0.85);
        color: #FFD700;
        padding: 8px 15px;
        border-radius: 8px;
        font-weight: bold;
        border: 2px solid #FFD700;
        box-shadow: 0 0 15px rgba(255,215,0,0.3);
    }}
    </style>
    
    <div class="track-container">
        <div class="distance-marker">⚠️ Obstacle: {obstacle_dist}m away</div>
        <div class="road">
    """
    
    for i in range(3):
        track_html += '<div class="lane">'
        
        # Show obstacle in its lane
        if i == obstacle_lane_idx and obstacle_dist > 0:
            track_html += '<div class="obstacle">🚧</div>'
        
        # Show sleek car in its lane
        if i == car_lane_idx:
            track_html += '''
            <div class="car">
                <div class="car-body">
                    <div class="car-window"></div>
                    <div class="car-stripe"></div>
                    <div class="car-wheel wheel-left"></div>
                    <div class="car-wheel wheel-right"></div>
                    <div class="car-wheel wheel-left-front"></div>
                    <div class="car-wheel wheel-right-front"></div>
                </div>
                <div class="car-glow"></div>
            </div>
            '''
        
        track_html += '</div>'
    
    track_html += """
        </div>
    </div>
    """
    
    st.markdown(track_html, unsafe_allow_html=True)
    
    # Lane indicator
    lanes = ["🟦 LEFT", "🟦 CENTER", "🟦 RIGHT"]
    lanes[car_lane_idx] = lanes[car_lane_idx].replace("🟦", "🟢")
    lanes[obstacle_lane_idx] = lanes[obstacle_lane_idx].replace("🟦", "🔴")
    
    col1, col2, col3 = st.columns(3)
    col1.markdown(f"### {lanes[0]}")
    col2.markdown(f"### {lanes[1]}")
    col3.markdown(f"### {lanes[2]}")


def render_game_over():
    """Game over screen"""
    st.markdown("""
    <style>
    .game-over-title {
        font-size: 50px;
        font-weight: bold;
        text-align: center;
        margin: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    is_high_score = st.session_state.leaderboard.add_score(st.session_state.score)
    
    if is_high_score:
        st.markdown('<div class="game-over-title">🏆 NEW HIGH SCORE! 🏆</div>', unsafe_allow_html=True)
        st.balloons()
    else:
        st.markdown('<div class="game-over-title">🏁 RACE FINISHED</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 📊 Race Statistics")
        
        stats_data = {
            "Final Score": st.session_state.score,
            "Distance Traveled": f"{int(st.session_state.distance)}m",
            "Questions Answered": st.session_state.questions_answered,
            "Correct Answers": st.session_state.correct_answers,
            "Accuracy": f"{int(st.session_state.correct_answers/max(st.session_state.questions_answered,1)*100)}%",
            "Max Streak": st.session_state.streak,
            "High Score": st.session_state.leaderboard.high_score
        }
        
        for label, value in stats_data.items():
            col_a, col_b = st.columns(2)
            col_a.markdown(f"**{label}:**")
            col_b.markdown(f"{value}")
        
        st.markdown("---")
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🔄 PLAY AGAIN", use_container_width=True, type="primary"):
                start_game()
                st.rerun()
        
        with col_b:
            if st.button("🏠 MAIN MENU", use_container_width=True):
                st.session_state.game_state = "menu"
                st.rerun()


# ===========================
# MAIN APP
# ===========================

def main():
    st.set_page_config(
        page_title="DSA Racing Simulator",
        page_icon="🏎️",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #1e1e2e 0%, #2d2d3d 100%);
    }
    .stButton>button {
        font-size: 18px;
        font-weight: bold;
        padding: 12px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    init_session_state()
    
    if st.session_state.game_state == "menu":
        render_menu()
    elif st.session_state.game_state == "playing":
        render_game()
    elif st.session_state.game_state == "game_over":
        render_game_over()


if __name__ == "__main__":
    main()