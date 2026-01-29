import streamlit as st
import time
import random
import os

# --- 1. 核心相容性修復 (模仿 Unit 18 架構) ---
def safe_rerun():
    """自動判斷並執行重整"""
    try:
        st.rerun()
    except AttributeError:
        try:
            st.experimental_rerun()
        except:
            st.stop()

# --- 關鍵修正：全自動檔案搜尋系統 ---
@st.cache_resource
def get_audio_file_map():
    """
    掃描專案內『所有資料夾』，建立 {檔名: 完整路徑} 的對照表。
    解決檔案放在子資料夾抓不到的問題。
    """
    file_map = {}
    # 從當前目錄 (.) 開始，向下搜尋每一層資料夾
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.lower().endswith(".m4a"):
                # 記錄檔名(小寫)與完整路徑的對應
                file_map[file.lower()] = os.path.join(root, file)
    return file_map

def safe_play_audio(filename):
    """
    播放音檔的安全函式
    1. 自動去地圖中找路徑
    2. 如果找不到，顯示溫馨提示
    """
    if not filename:
        return

    # 取得檔案地圖
    audio_map = get_audio_file_map()
    target_key = filename.lower()

    # 檢查檔案是否存在於地圖中
    if target_key in audio_map:
        full_path = audio_map[target_key]
        try:
            with open(full_path, "rb") as f:
                audio_bytes = f.read()
            st.audio(audio_bytes, format='audio/mp4')
        except Exception as e:
            st.error(f"播放失敗: {e}")
    else:
        # 找不到檔案時的處理
        st.warning(f"⚠️ 找不到音檔: {filename}")
        st.caption("請確認檔案是否已上傳到 GitHub 或專案資料夾中")

# --- 0. 系統配置 ---
st.set_page_config(page_title="Kaolahan 所喜歡的", page_icon="🍲", layout="centered")

# --- CSS 美化 (改為暖橘色系，對應 Unit 18 的排版) ---
st.markdown("""
    <style>
    body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    .source-tag { font-size: 12px; color: #aaa; text-align: right; font-style: italic; }
    
    /* 單字卡 */
    .word-card {
        background: linear-gradient(135deg, #FFF3E0 0%, #ffffff 100%);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 15px;
        border-bottom: 4px solid #FF7043;
    }
    .emoji-icon { font-size: 48px; margin-bottom: 10px; }
    .amis-text { font-size: 22px; font-weight: bold; color: #E64A19; }
    .chinese-text { font-size: 16px; color: #795548; }
    
    /* 句子框 */
    .sentence-box {
        background-color: #FFF8E1;
        border-left: 5px solid #FFA000;
        padding: 15px;
        margin: 10px 0;
        border-radius: 0 10px 10px 0;
    }

    /* 按鈕 */
    .stButton>button {
        width: 100%; border-radius: 12px; font-size: 20px; font-weight: 600;
        background-color: #FFCCBC; color: #BF360C; border: 2px solid #FF7043; padding: 12px;
    }
    .stButton>button:hover { background-color: #FFAB91; border-color: #E64A19; }
    .stProgress > div > div > div > div { background-color: #FF7043; }
    </style>
""", unsafe_allow_html=True)

# --- 2. 資料庫 (Kaolahan 內容) ---
# 注意：dateng.m4a 和 kohaw.m4a 在您的上傳清單中缺席，這裡保留是為了完整性
vocab_data = [
    {"amis": "Kaolahan", "chi": "所喜歡的", "icon": "❤️", "source": "核心單字", "audio": "kaolahan.m4a"},
    {"amis": "Facidol", "chi": "麵包樹果", "icon": "🍈", "source": "食材", "audio": "facidol.m4a"},
    {"amis": "Haca", "chi": "也 / 亦", "icon": "➕", "source": "連接詞", "audio": "haca.m4a"},
    {"amis": "Maemin", "chi": "全部 / 所有的", "icon": "💯", "source": "數量", "audio": "maemin.m4a"},
    {"amis": "Sikaen", "chi": "菜餚 / 配菜", "icon": "🍱", "source": "食物", "audio": "sikaen.m4a"},
    {"amis": "Dateng", "chi": "菜 / 野菜", "icon": "🥬", "source": "食物", "audio": "dateng.m4a"}, # 缺檔
    {"amis": "Kohaw", "chi": "湯", "icon": "🍲", "source": "食物", "audio": "kohaw.m4a"},   # 缺檔
    {"amis": "Mato’asay", "chi": "老人 / 長輩", "icon": "👵", "source": "人物", "audio": "matoasay.m4a"},
]

sentences = [
    {"amis": "O maan ko kaolahan iso a sikaen?", "chi": "你喜歡什麼樣的菜呢？", "icon": "❓", "source": "問句", "audio": "sentence_01.m4a"},
    {"amis": "O foting ko kaolahan ako a dateng.", "chi": "魚是我最喜歡的菜。", "icon": "🐟", "source": "回答", "audio": "sentence_02.m4a"},
    {"amis": "Kaolahan no wama konini a kohaw.", "chi": "這碗是爸爸最喜歡的湯。", "icon": "👨", "source": "描述", "audio": "sentence_03.m4a"},
    {"amis": "Tadakaolahan no mato’asay kona dateng.", "chi": "這些是老人家最喜歡的菜。", "icon": "👵", "source": "描述", "audio": "sentence_04.m4a"},
    {"amis": "Kaolahan ako a maemin konini a sikaen.", "chi": "這些都是我最喜歡的菜餚。", "icon": "😋", "source": "感嘆", "audio": "sentence_05.m4a"},
    {"amis": "O facidol i, o tadakaolahan haca no ’Amis.", "chi": "麵包樹果也是阿美族人最愛。", "icon": "🍈", "source": "文化", "audio": "sentence_06.m4a"},
]

# --- 3. 隨機題庫 (Kaolahan 內容) ---
raw_quiz_pool = [
    {
        "q": "「麵包樹果」的阿美語怎麼說？",
        "audio": "facidol.m4a",
        "options": ["Facidol", "Foting", "Dateng"],
        "ans": "Facidol",
        "hint": "阿美族人最愛的食材之一"
    },
    {
        "q": "O maan ko kaolahan iso a sikaen?",
        "audio": "sentence_01.m4a",
        "options": ["你喜歡什麼樣的菜呢？", "這是誰煮的菜？", "你要去哪裡買菜？"],
        "ans": "你喜歡什麼樣的菜呢？",
        "hint": "Maan 是「什麼」，Kaolahan 是「喜歡的」"
    },
    {
        "q": "Kaolahan no wama konini a kohaw.",
        "audio": "sentence_03.m4a",
        "options": ["這碗是爸爸最喜歡的湯", "這碗是媽媽煮的湯", "我不喜歡喝湯"],
        "ans": "這碗是爸爸最喜歡的湯",
        "hint": "Wama 是爸爸，Kohaw 是湯"
    },
    {
        "q": "單字測驗：Maemin",
        "audio": "maemin.m4a",
        "options": ["全部", "一點點", "沒有"],
        "ans": "全部",
        "hint": "Kaolahan ako a maemin (這些「全部」都是我喜歡的)"
    },
    {
        "q": "單字測驗：Mato’asay",
        "audio": "matoasay.m4a",
        "options": ["老人/長輩", "小孩", "年輕人"],
        "ans": "老人/長輩",
        "hint": "Tadakaolahan no mato’asay (老人家最喜歡的)"
    },
    {
        "q": "O foting ko kaolahan ako a dateng.",
        "audio": "sentence_02.m4a",
        "options": ["魚是我最喜歡的菜", "我喜歡吃麵包樹果", "這道菜很鹹"],
        "ans": "魚是我最喜歡的菜",
        "hint": "Foting 是魚"
    },
    {
        "q": "「湯」的阿美語是？",
        "audio": "kohaw.m4a",
        "options": ["Kohaw", "Dateng", "Sapaiyo"],
        "ans": "Kohaw",
        "hint": "喝熱熱的 Kohaw"
    }
]

# --- 4. 狀態初始化 (Unit 18 洗牌邏輯) ---
if 'init' not in st.session_state:
    st.session_state.score = 0
    st.session_state.current_q_idx = 0
    st.session_state.quiz_id = str(random.randint(1000, 9999))
    
    # 抽題與洗牌
    selected_questions = random.sample(raw_quiz_pool, 4)
    final_questions = []
    for q in selected_questions:
        q_copy = q.copy()
        shuffled_opts = random.sample(q['options'], len(q['options']))
        q_copy['shuffled_options'] = shuffled_opts
        final_questions.append(q_copy)
        
    st.session_state.quiz_questions = final_questions
    st.session_state.init = True

# --- 5. 主介面 ---
st.markdown("<h1 style='text-align: center; color: #BF360C;'>Kaolahan 所喜歡的</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8D6E63;'>講師：高春美 | 教材提供者：高春美</p>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📖 詞彙與句型", "🎲 隨機挑戰"])

# === Tab 1: 學習模式 ===
with tab1:
    st.subheader("📝 核心單字")
    col1, col2 = st.columns(2)
    for i, word in enumerate(vocab_data):
        with (col1 if i % 2 == 0 else col2):
            st.markdown(f"""
            <div class="word-card">
                <div class="emoji-icon">{word['icon']}</div>
                <div class="amis-text">{word['amis']}</div>
                <div class="chinese-text">{word['chi']}</div>
                <div class="source-tag">{word['source']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"🔊 播放", key=f"btn_vocab_{i}"):
                safe_play_audio(word['audio'])

    st.markdown("---")
    st.subheader("🗣️ 實用句型")
    for i, sent in enumerate(sentences):
        st.markdown(f"""
        <div class="sentence-box">
            <div style="font-size: 20px; color: #E65100; font-weight: bold;">{sent['icon']} {sent['amis']}</div>
            <div style="font-size: 16px; color: #5D4037; margin-top: 5px;">{sent['chi']}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"▶️ 朗讀句子", key=f"btn_sent_{i}"):
            safe_play_audio(sent['audio'])

# === Tab 2: 測驗模式 ===
with tab2:
    st.subheader("🧠 隨機測驗 (共4題)")
    
    current_idx = st.session_state.current_q_idx
    questions = st.session_state.quiz_questions
    
    if current_idx < len(questions):
        q_data = questions[current_idx]
        progress = (current_idx / len(questions))
        st.progress(progress)
        
        st.markdown(f"### Q{current_idx + 1}: {q_data['q']}")
        
        # 播放題目語音
        if q_data.get('audio'):
            if st.button("🔊 聽題目發音", key=f"quiz_audio_{current_idx}"):
                safe_play_audio(q_data['audio'])
        
        option_cols = st.columns(len(q_data['shuffled_options']))
        
        if f"answered_{current_idx}" not in st.session_state:
            for idx, opt in enumerate(q_data['shuffled_options']):
                if st.button(opt, key=f"opt_{current_idx}_{idx}"):
                    if opt == q_data['ans']:
                        st.session_state.score += 25
                        st.success(f"🎉 正確！ {q_data['ans']}")
                    else:
                        st.error(f"❌ 答錯了，正確答案是：{q_data['ans']}")
                        st.info(f"💡 提示：{q_data['hint']}")
                    
                    st.session_state[f"answered_{current_idx}"] = True
                    time.sleep(1.5)
                    st.session_state.current_q_idx += 1
                    safe_rerun()
        else:
            st.info("載入下一題中...")
            
    else:
        st.progress(1.0)
        st.balloons()
        final_score = st.session_state.score
        
        st.markdown(f"""
        <div style="text-align: center; padding: 30px; background-color: #FFF3E0; border-radius: 20px;">
            <h2 style="color: #E64A19;">測驗完成！</h2>
            <h1 style="font-size: 60px; color: #BF360C;">{final_score} 分</h1>
            <p>Kaolahan iso konini a app? (你喜歡這個App嗎？)</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 再玩一次"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            safe_rerun()
