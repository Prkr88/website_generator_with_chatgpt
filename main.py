import openai
import os
import uuid
import webbrowser

MODEL_ENGINE = "text-davinci-003"
MAX_TOKENS = 2048
openai.api_key = os.getenv('OPEN_AI_API_KEY')


def generate_plain_response(prompt):
    print(prompt)
    completion = openai.Completion.create(
        engine=MODEL_ENGINE,
        prompt=prompt,
        max_tokens=MAX_TOKENS,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return completion.choices[0].text


def generate_response_with_context(prompt, context):
    print('context: %s \n\n prompt: %s' % (context, prompt))
    completion = openai.Completion.create(
        engine=MODEL_ENGINE,
        prompt="context:" + context + "\n\n" + "prompt:" + prompt,
        max_tokens=MAX_TOKENS,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return completion.choices[0].text


def generate_html():
    prompt = "create an html web page for a site about breeds of cats with bootstrap 5. the site should have " \
             "a bootstarp nav bar with: CatBreeds brand name about, contact and blog. the first section should represent the site" \
             "idea and vision, the passion of the owner about cats in 300 words. the second section should contain" \
             "a bootstrap carousel with 3 breads of cats each with its photo from picsum.photos and description the carousel should have " \
             "navigation buttons. " \
             "the last section should contain a footer with all the contact information." \
             "style the site with css to make it approachable and convenient. do not include integrity checks for " \
             "scripts you add the web site" \
             "check that you have </html> closing tag at the end of the site, if not keep generating the content."

    html_content = generate_plain_response(prompt)
    for i in range(0, 10):
        answer = html_feedback_loop(html_content,
                                    "if the html in the context is valid return Yes else complete the missing parts in the page")
        if "Yes" in answer:
            break
        else:
            html_content = answer

    return html_content


def html_feedback_loop(prompt, html):
    response = generate_response_with_context(prompt, html)
    print(response)
    return response


def save_html_file(content):
    html_file_name = 'mySite' + str(uuid.uuid4()) + '.html'
    with open(html_file_name, 'w') as f:
        f.write(content)
    return html_file_name


def open_file_in_browser(file_name):
    filename = 'file:///' + os.getcwd() + '/' + file_name
    webbrowser.open_new_tab(filename)


if __name__ == '__main__':
    html_content = generate_html()
    html_file_name = save_html_file(html_content)
    open_file_in_browser(html_file_name)
