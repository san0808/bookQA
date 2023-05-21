from PyPDF2 import PdfReader
import re
import json

def extract_conversations_from_pdf(pdf_path):
    pdf_reader = PdfReader(pdf_path)

    conversations = [
        
    ]
    
    current_speaker = None
    current_conversation = []

    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text = page.extract_text()

        # Identify conversation boundaries based on patterns
        dialogue_pattern = re.compile(r'([A-Z\s]+):')
        dialogue_matches = dialogue_pattern.findall(text)

        for match in dialogue_matches:
            speaker = match.strip()

            # Start a new conversation if a new speaker is detected
            if speaker != current_speaker:
                if current_conversation:
                    conversations.append(current_conversation)
                current_speaker = speaker
                current_conversation = []

            # Extract the message
            message = text[text.index(speaker) + len(speaker):].strip()

            # Clean and preprocess the message if needed

            # Add the message to the current conversation
            current_conversation.append({
                "speaker": speaker,
                "message": message
            })

    # Add the last conversation to the list
    if current_conversation:
        conversations.append(current_conversation)

    # Convert the conversations into the desired format and save as JSON
    training_examples = []
    for conversation in conversations:
        for i in range(1, len(conversation)):
            training_examples.append({
                "context": [exchange["message"] for exchange in conversation[:i]],
                "target": conversation[i]["message"]
            })

    # Save the training examples to a JSON file
    with open("training_examples.json", "w") as file:
        json.dump(training_examples, file, indent=4)

pdf_path = "resources\The Courage To Be Disliked How to free yourself... (Z-Library).pdf"
extract_conversations_from_pdf(pdf_path)
