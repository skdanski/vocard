# VoCard
An iOS Application focused on helping users learn English Vocabulary words with the help of the Forgetting Curve and AI tools.
This project was part of SKKU 2023 Fall Semester's Capstone Design Course
# Features
1. Sleek Card-based UI/UX Design
2. ChatGPT & Dall-E Integration
   - ChatGPT used to provide feedback on user inputted example sentences for any vocabulary word.
   - Dall-E 3 used to provide visual feedback based on user inputted example sentences.
     - Images generated regardless of the correctness of the sentence
# Requirements
1. Mac OS (for Swift UI)
2. OpenAI API key
# Try it Yourself
## Testing the APIs
   ```
   # Requirements installation
   python3 -m pip install -r requirements.txt

   # initialize local django server
   py manage.py runserver

   # API documentation on Swagger
   localhost:port/api/schema/swagger-ui/#/
   ```
