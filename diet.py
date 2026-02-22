import os
import gradio as gr
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ---------- GEMINI FUNCTION ----------
def get_gemini_response(prompt, image=None):
    model = genai.GenerativeModel("gemini-2.5-flash")

    content = [prompt]

    if image:
        content.append(Image.open(image))

    response = model.generate_content(content)
    return response.text


# ---------- MEAL PLAN ----------
def generate_meal_plan(goals, conditions, routines, preferences, restrictions, extra):

    profile = f"""
    Goals: {goals}
    Conditions: {conditions}
    Routine: {routines}
    Preferences: {preferences}
    Restrictions: {restrictions}
    """

    prompt = f"""
    Act as a professional dietitian.

    Create a 7-day personalized meal plan.

    USER PROFILE:
    {profile}

    ADDITIONAL NEEDS:
    {extra}
    """

    return get_gemini_response(prompt)


# ---------- FOOD ANALYSIS ----------
def analyze_food(image):
    prompt = """
    Analyze the food and provide calories, macros and health tips.
    """
    return get_gemini_response(prompt, image)


# ---------- HEALTH INSIGHTS ----------
def health_insight(question, goals, conditions, routines, preferences, restrictions):

    profile = f"""
    Goals: {goals}
    Conditions: {conditions}
    Routine: {routines}
    Preferences: {preferences}
    Restrictions: {restrictions}
    """

    prompt = f"""
    USER PROFILE:
    {profile}

    QUESTION:
    {question}
    """

    return get_gemini_response(prompt)


# ---------- UI ----------
with gr.Blocks(title="NutriSmart AI") as app:

    gr.Markdown("## 🥗 NutriSmart – AI Health Companion")

    with gr.Accordion("👤 Health Profile", open=False):

        goals = gr.Textbox(label="Health Goals")
        conditions = gr.Textbox(label="Medical Conditions")
        routines = gr.Textbox(label="Fitness Routine")
        preferences = gr.Textbox(label="Food Preferences")
        restrictions = gr.Textbox(label="Dietary Restrictions")

    with gr.Tab("🥗 Meal Planner"):

        extra = gr.Textbox(label="Meal Planning Needs")
        meal_output = gr.Markdown()
        meal_btn = gr.Button("Generate Meal Plan")

        meal_btn.click(
            generate_meal_plan,
            inputs=[goals, conditions, routines, preferences, restrictions, extra],
            outputs=meal_output
        )

    with gr.Tab("📸 Food Analysis"):

        food_img = gr.Image(type="filepath")
        food_output = gr.Markdown()
        food_btn = gr.Button("Analyze Food")

        food_btn.click(analyze_food, inputs=food_img, outputs=food_output)

    with gr.Tab("🧠 Health Insights"):

        question = gr.Textbox(label="Ask your health question")
        health_output = gr.Markdown()
        health_btn = gr.Button("Get Insights")

        health_btn.click(
            health_insight,
            inputs=[question, goals, conditions, routines, preferences, restrictions],
            outputs=health_output
        )

app.launch()