import streamlit as st
import auth_functions
from io import StringIO
import pymupdf
import requests
from streamlit_pdf_viewer import pdf_viewer
from jinja2 import Environment, FileSystemLoader
import pdfkit
import json

## -------------------------------------------------------------------------------------------------
## Not logged in -----------------------------------------------------------------------------------
## -------------------------------------------------------------------------------------------------
if False:
    pass
# if 'user_info' not in st.session_state:
#     col1,col2,col3 = st.columns([1,2,1])

#     # Authentication form layout
#     do_you_have_an_account = col2.selectbox(label='Do you have an account?',options=('Yes','No','I forgot my password'))
#     auth_form = col2.form(key='Authentication form',clear_on_submit=False)
#     email = auth_form.text_input(label='Email')
#     password = auth_form.text_input(label='Password',type='password') if do_you_have_an_account in {'Yes','No'} else auth_form.empty()
#     auth_notification = col2.empty()

#     # Sign In
#     if do_you_have_an_account == 'Yes' and auth_form.form_submit_button(label='Sign In',use_container_width=True,type='primary'):
#         with auth_notification, st.spinner('Signing in'):
#             auth_functions.sign_in(email,password)

#     # Create Account
#     elif do_you_have_an_account == 'No' and auth_form.form_submit_button(label='Create Account',use_container_width=True,type='primary'):
#         with auth_notification, st.spinner('Creating account'):
#             auth_functions.create_account(email,password)

#     # Password Reset
#     elif do_you_have_an_account == 'I forgot my password' and auth_form.form_submit_button(label='Send Password Reset Email',use_container_width=True,type='primary'):
#         with auth_notification, st.spinner('Sending password reset link'):
#             auth_functions.reset_password(email)

#     # Authentication success and warning messages
#     if 'auth_success' in st.session_state:
#         auth_notification.success(st.session_state.auth_success)
#         del st.session_state.auth_success
#     elif 'auth_warning' in st.session_state:
#         auth_notification.warning(st.session_state.auth_warning)
#         del st.session_state.auth_warning

## -------------------------------------------------------------------------------------------------
## Logged in --------------------------------------------------------------------------------------
## -------------------------------------------------------------------------------------------------
else:
    # # Show user information
    # st.header('User information:')
    # st.write(st.session_state.user_info)

    # # Sign out
    # st.header('Sign out:')
    # st.button(label='Sign Out',on_click=auth_functions.sign_out,type='primary')

    # # Delete Account
    # st.header('Delete account:')
    # password = st.text_input(label='Confirm your password',type='password')
    # st.button(label='Delete Account',on_click=auth_functions.delete_account,args=[password],type='primary')

    # Resume agent
    uploaded_file = st.file_uploader("Upload your resume pdf", type="pdf")
    if uploaded_file is not None:
        content = uploaded_file.read()

        # display pdf file as text
        pdf_viewer(content)

        # extract text from pdf
        pdf = pymupdf.open(stream=content, filetype="pdf")
        text = ""
        for page in pdf:
            text += page.get_text()
        pdf.close()
        
        # send request to api to extract json data
        st.header("Server response:")
        with st.spinner('Waiting for server response...'):
            # make a post request using query text
            response = requests.post(st.secrets["SERVER_URL"]+ "/parse_resume_text", params={"text": text})
            response_json = response.json()

            # # mock up for testing
            # response_json = json.loads(open('./data/my_resume_parsed.json').read())
            # st.write(response_json)

        # create the new resume using template
        env = Environment(loader=FileSystemLoader('./templates'))
        template = env.get_template('template2.html')
        new_resume_html = template.render(data=response_json)

        # convert html to pdf
        config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
        options = {
            'page-size': 'A4',
            'margin-top': '0mm',
            'margin-right': '0mm',
            'margin-bottom': '0mm',
            'margin-left': '0mm',
            'encoding': "UTF-8",
            'no-outline': None,
            'no-images': True,
            'disable-external-links': True,
            'disable-javascript': True
        }
        new_resume_pdf = pdfkit.from_string(new_resume_html, False, options=options, configuration=config)
        

        # download button
        st.download_button(
            label="Download the updated resume",
            data=new_resume_pdf,
            file_name="updated_resume.pdf",
            mime="text/pdf",
        )

        # display the updated resume
        pdf_viewer(new_resume_pdf)


    
