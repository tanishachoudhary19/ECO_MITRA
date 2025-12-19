# import os
# from flask import Flask, render_template, request, redirect, url_for, session
# from werkzeug.utils import secure_filename
# from dotenv import load_dotenv
# import google.generativeai as genai   # ✅ Gemini client

# # ------------------- LOAD ENV VARIABLES -------------------
# load_dotenv()

# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "default_secret_key")

# if not GOOGLE_API_KEY:
#     raise ValueError("❌ GOOGLE_API_KEY is not set in .env file.")

# # ------------------- INIT GEMINI CLIENT -------------------
# genai.configure(api_key=GOOGLE_API_KEY)
# model = genai.GenerativeModel("gemini-pro")   # ✅ fast + free tier supported

# def gemini_query(query: str) -> str:
#     """Query Gemini and return response text."""
#     try:
#         response = model.generate_content(query)
#         return response.text.strip() if response and response.text else "⚠️ No response from Gemini."
#     except Exception as e:
#         return f"⚠️ Error: {str(e)}"

# # ------------------- FLASK SETUP -------------------
# app = Flask(__name__)
# app.secret_key = FLASK_SECRET_KEY  

# # Upload settings
# UPLOAD_FOLDER = 'data/uploads'
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)

# def allowed_file(filename):
#     """Check allowed file extensions."""
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# # ------------------- ROUTES -------------------

# @app.route('/')
# def home():
#     return render_template('home.html')

# # ✅ Show EcoMeter page (GET)
# @app.route('/ecometer', methods=['GET'])
# def ecometer_page():
#     return render_template('ecometer.html')

# # ✅ Handle file upload &/or manual product name (POST)
# @app.route('/ecometer/analyze', methods=['POST'])
# def analyze_file():
#     file = request.files.get('file')
#     product_name = request.form.get('product_name')

#     if product_name:
#         product_to_send = product_name
#     elif file and file.filename != '' and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         file.save(filepath)
#         product_to_send = filename  # Use filename as placeholder
#     else:
#         return render_template('ecometer.html', results=[{
#             "name": "N/A",
#             "carbon_emission": "❌ Please enter a product name or upload a valid image (PNG/JPG/JPEG)."
#         }])

#     # Request structured JSON from Gemini
#     query = (
#         f"For the product '{product_to_send}', estimate the carbon emissions in kg CO2e. "
#         f"Return a concise JSON object with these fields: embodied_emissions, usage_emissions, total_emissions, summary. "
#         f"Example: {{'embodied_emissions': 0.35, 'usage_emissions': 0.028, 'total_emissions': 0.378, 'summary': 'A Red Bull can has a total estimated carbon footprint of 0.378 kg CO2e, mainly due to aluminum production and refrigeration.'}}."
#     )
#     import json
#     agent_response = gemini_query(query)
#     result = None
#     try:
#         start = agent_response.find('{')
#         end = agent_response.rfind('}') + 1
#         if start != -1 and end != -1:
#             result = json.loads(agent_response[start:end])
#     except Exception:
#         result = None

#     analysis_results = [{
#         "name": product_to_send,
#         "carbon_emission": result if result else agent_response
#     }]

#     return render_template('ecometer.html', results=analysis_results)

# # 🔹 DIY Assistant handled by Gemini
# @app.route('/diy_assistant')
# def diy_assistant_page():
#     return render_template('diy_assistant.html')

# @app.route('/diy_assistant_submit', methods=['POST'])
# def diy_assistant_submit():
#     product_name = request.form.get('product_name')
#     if not product_name:
#         return "Product name is required!", 400

#     query = (
#         f"Suggest at least 3 creative DIY reuse ideas for {product_name}. "
#         f"For each idea, provide: 'title', 'description', and 'difficulty' (Easy, Medium, Hard). Do not include image URLs. "
#         f"Return the result as a JSON array. Example: [{{'title': 'Spray Bottle', 'description': 'Turn the bottle into a spray bottle for plants.', 'difficulty': 'Easy'}}, ...]"
#     )
#     import json
#     from src.unsplash_api import get_unsplash_image
#     diy_raw = gemini_query(query)
#     diy_ideas = []
#     try:
#         start = diy_raw.find('[')
#         end = diy_raw.rfind(']') + 1
#         if start != -1 and end != -1:
#             diy_ideas = json.loads(diy_raw[start:end])
#     except Exception:
#         diy_ideas = [{"title": "DIY Idea", "description": diy_raw, "difficulty": ""}]

#     # Fetch Unsplash image for each idea
#     for idea in diy_ideas:
#         # Make search query more specific for DIY crafts
#         search_query = f"DIY {product_name} {idea.get('title', '')} craft upcycle project"
#         image_url = get_unsplash_image(search_query)
#         idea['image_url'] = image_url or ""

#     return render_template(
#         'diy_assistant.html',
#         diy_ideas=diy_ideas,
#         product_name=product_name
#     )

# # ------------------- CART ROUTES -------------------
# @app.route('/add_to_cart', methods=['POST'])
# def add_to_cart():
#     item_name = request.form.get('item_name')
#     if item_name:
#         if 'cart' not in session:
#             session['cart'] = []
#         session['cart'].append(item_name)
#     return redirect(url_for('ecometer_page'))

# @app.route('/view_cart')
# def view_cart():
#     cart_items = session.get('cart', [])
#     return render_template('view_cart.html', cart_items=cart_items)

# # ------------------- MAIN -------------------
# @app.route('/health_report', methods=['GET', 'POST'])
# def health_report():
#     health_report = None
#     product_name = None
#     if request.method == 'POST':
#         product_name = request.form.get('product_name')
#         file = request.files.get('file')
#         # Optionally save the uploaded image
#         if file and file.filename != '' and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             file.save(filepath)
#         if not product_name:
#             health_report = "Please provide a product name."
#         else:
#                 query = (
#                     f"For the product '{product_name}', generate a structured health impact report in JSON format with these fields: "
#                     f"nutrition (total fat, sodium, total carbs), good_ingredients (list), ingredients_to_consider (list), health_tips (list). "
#                     f"Base the report on typical carbon emissions and health effects for an individual and community. "
#                     f"Example format: {{'nutrition': {{'total_fat': 0, 'sodium': 140, 'total_carbs': 2}}, 'good_ingredients': [...], 'ingredients_to_consider': [...], 'health_tips': [...]}}."
#                 )
#                 import json
#                 response = gemini_query(query)
#                 report = None
#                 try:
#                     # Try to extract JSON from Gemini response
#                     start = response.find('{')
#                     end = response.rfind('}') + 1
#                     if start != -1 and end != -1:
#                         report = json.loads(response[start:end])
#                 except Exception:
#                     report = None
#                 health_report = report if report else response
#     return render_template('health_report.html', health_report=health_report, product_name=product_name)

# # ------------------- MAIN -------------------
# if __name__ == '__main__':
#     app.run(debug=True)



import os
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from groq import Groq
import json

# ------------------- LOAD ENV VARIABLES -------------------
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "default_secret_key")

if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY is not set in .env file.")

# ------------------- INIT GROQ CLIENT -------------------
groq_client = Groq(api_key=GROQ_API_KEY)

def llm_query(query: str) -> str:
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant specializing in environmental and health data. When asked for JSON, return ONLY valid JSON without any markdown formatting, code blocks, or additional text. Do not wrap JSON in ```json tags."
                },
                {
                    "role": "user",
                    "content": query
                }
            ],
            temperature=0.2
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# ------------------- FLASK SETUP -------------------
app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY

UPLOAD_FOLDER = 'data/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ------------------- ROUTES -------------------

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/ecometer', methods=['GET'])
def ecometer_page():
    return render_template('ecometer.html')

@app.route('/ecometer/analyze', methods=['POST'])
def analyze_file():
    file = request.files.get('file')
    product_name = request.form.get('product_name')

    if product_name:
        product_to_send = product_name
    elif file and file.filename != '' and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        product_to_send = filename
    else:
        return render_template('ecometer.html', results=[{
            "name": "N/A",
            "carbon_emission": "❌ Please enter a product name or upload a valid image."
        }])

    query = (
        f"For the product '{product_to_send}', estimate the carbon emissions in kg CO2e. "
        f"Return ONLY a valid JSON object with these exact fields: embodied_emissions (number), usage_emissions (number), total_emissions (number), summary (string). "
        f"Do not include any markdown formatting or extra text. "
        f"Example format: {{\"embodied_emissions\": 0.18, \"usage_emissions\": 0.02, \"total_emissions\": 0.2, \"summary\": \"A typical plastic bottle has an estimated carbon footprint of 0.20 kg CO2e, primarily from plastic production and transportation. Usage emissions depend on if it is reused, and if it is, the emissions are minimal.\"}}"
    )

    response = llm_query(query)
    result = None

    try:
        start = response.find('{')
        end = response.rfind('}') + 1
        if start != -1 and end != -1:
            result = json.loads(response[start:end])
    except Exception:
        result = None

    analysis_results = [{
        "name": product_to_send,
        "carbon_emission": result if result else response
    }]

    return render_template('ecometer.html', results=analysis_results)

# ------------------- DIY ASSISTANT -------------------

@app.route('/diy_assistant')
def diy_assistant_page():
    return render_template('diy_assistant.html')

@app.route('/diy_assistant_submit', methods=['POST'])
def diy_assistant_submit():
    product_name = request.form.get('product_name')
    if not product_name:
        return "Product name is required!", 400

    query = (
        f"Suggest at least 3 creative DIY reuse ideas for {product_name}. "
        f"For each idea, provide: 'title' (string), 'description' (string), and 'difficulty' (Easy, Medium, or Hard). "
        f"Do not include image URLs or any markdown formatting. "
        f"Return ONLY a valid JSON array. "
        f"Example format: [{{\"title\": \"Spray Bottle\", \"description\": \"Turn the bottle into a spray bottle for plants.\", \"difficulty\": \"Easy\"}}, {{\"title\": \"Bird Feeder\", \"description\": \"Cut holes and fill with birdseed.\", \"difficulty\": \"Medium\"}}]"
    )

    from src.unsplash_api import get_unsplash_image

    response = llm_query(query)
    diy_ideas = []

    try:
        start = response.find('[')
        end = response.rfind(']') + 1
        if start != -1 and end != -1:
            diy_ideas = json.loads(response[start:end])
    except Exception:
        diy_ideas = [{"title": "DIY Idea", "description": response, "difficulty": ""}]

    for idea in diy_ideas:
        search_query = f"DIY {product_name} {idea.get('title', '')} upcycle"
        idea['image_url'] = get_unsplash_image(search_query) or ""

    return render_template(
        'diy_assistant.html',
        diy_ideas=diy_ideas,
        product_name=product_name
    )

# ------------------- CART -------------------

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    item_name = request.form.get('item_name')
    if item_name:
        session.setdefault('cart', []).append(item_name)
    return redirect(url_for('ecometer_page'))

@app.route('/view_cart')
def view_cart():
    return render_template('view_cart.html', cart_items=session.get('cart', []))

# ------------------- HEALTH REPORT -------------------

@app.route('/health_report', methods=['GET', 'POST'])
def health_report():
    health_report = None
    product_name = None

    if request.method == 'POST':
        product_name = request.form.get('product_name')
        if not product_name:
            health_report = "Please provide a product name."
        else:
            query = (
                f"Analyze the specific product '{product_name}' and generate a detailed, customized health impact report. "
                f"Return ONLY valid JSON with these exact fields: "
                f"1. nutrition: object with total_fat (grams), sodium (mg), total_carbs (grams), calories (number). If '{product_name}' is not edible, set all to 0. "
                f"2. good_ingredients: array of beneficial ingredients/materials specifically found in '{product_name}'. "
                f"3. ingredients_to_consider: array of specific concerning ingredients/materials in '{product_name}' with detailed health/safety explanations. "
                f"4. health_tips: array of 3-4 actionable health recommendations specifically for '{product_name}'. "
                f"IMPORTANT: Analyze what '{product_name}' actually is (food/beverage/packaging/electronics/clothing etc.) and provide accurate, product-specific information. "
                f"Do NOT use generic examples. Tailor ALL content to '{product_name}'. No markdown formatting. "
                f"JSON format: {{\"nutrition\": {{\"total_fat\": 0, \"sodium\": 0, \"total_carbs\": 0, \"calories\": 0}}, \"good_ingredients\": [\"...\"], \"ingredients_to_consider\": [\"...\"], \"health_tips\": [\"...\"]}}"
            )

            response = llm_query(query)
            report = None

            try:
                start = response.find('{')
                end = response.rfind('}') + 1
                if start != -1 and end != -1:
                    report = json.loads(response[start:end])
            except Exception:
                report = None

            health_report = report if report else response

    return render_template(
        'health_report.html',
        health_report=health_report,
        product_name=product_name
    )

# ------------------- MAIN -------------------
if __name__ == '__main__':
    app.run(debug=True)
