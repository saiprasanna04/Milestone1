import google.generativeai as genai
import pandas as pd
import json
import os

def analyze_call_and_update_crm(call_text, phone_number, crm_excel_path, api_key, model_name="gemini-pro"):
    """
    Analyze call text using Gemini API and update CRM Excel file with post-call analysis.

    Args:
        call_text (str): Text containing the call details.
        phone_number (str): Phone number to identify the contact in the CRM.
        crm_excel_path (str): Path to the CRM data Excel file.
        api_key (str): Gemini API key.
        model_name (str, optional): The name of the Gemini model to use. Defaults to "gemini-pro".

    Returns:
        str: Success message or error message.
    """
    genai.configure(api_key='hf_YYKuTzNDzLsmSy.....ceqbGtXExFpU')
    model = genai.GenerativeModel(model_name)

    try:
    
        crm_df = pd.read_excel(crm_excel_path)

        if "post call analysis" not in crm_df.columns:
            crm_df["post call analysis"] = ""

    
        contact_row = crm_df[crm_df["phone_number"].astype(str) == str(phone_number)]

        if contact_row.empty:
            return "Error: No matching contact found for the provided phone number."

        prompt_extraction = f"""
        Analyze the following call text and extract the following attributes:
        - Sentiment
        - Tone
        - Intent
        - Pitch
        - Key Discussions

        Call Text: {call_text}

        Respond strictly in JSON format like this:
        {{
            "sentiment": "positive",
            "tone": "formal",
            "intent": "complaint",
            "pitch": "high",
            "key_discussions": "feedback on UI and functionalities"
        }}
        """

        try:
            extraction_response = model.generate_content(prompt_extraction)
            print("Gemini API Extraction Response:", extraction_response.text)  # Debugging
            extracted_details = json.loads(extraction_response.text)
        except json.JSONDecodeError:
            return "Error: The Gemini API response is not valid JSON. Please check the response format."
        except Exception as e:
            return f"Error during extraction with Gemini API: {e}"

        prompt_analysis = f"""
        Based on the following extracted details and CRM data, generate a post-call analysis:

        Extracted Details:
        Sentiment: {extracted_details['sentiment']}
        Tone: {extracted_details['tone']}
        Intent: {extracted_details['intent']}
        Pitch: {extracted_details['pitch']}
        Key Discussions: {extracted_details['key_discussions']}

        CRM Data:
        {contact_row.to_string(index=False)}

        Provide the analysis in a concise and actionable manner.
        """

        try:
            analysis_response = model.generate_content(prompt_analysis)
            post_call_analysis = analysis_response.text.strip()
            print("post-call-summary: " + str(post_call_analysis))
        except Exception as e:
            return f"Error during post-call analysis generation with Gemini API: {e}"

        crm_df.loc[crm_df["phone_number"].astype(str) == str(phone_number), "post call analysis"] = post_call_analysis

        crm_df.to_excel(crm_excel_path, index=False)
        return "Post call analysis successfully updated in the CRM file."

    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    sample_call_text = "This is very bad product. You should work more on the UI and functionalities."
    sample_phone_number = "001-601-522-0792"
    crm_data_path = "crm_data.xlsx"  # Path to uploaded CRM Excel file
    gemini_api_key = os.environ.get("GEMINI_API_KEY")  # Replace with your Gemini API key

    result = analyze_call_and_update_crm(sample_call_text, sample_phone_number, crm_data_path, gemini_api_key)
    print(result)
