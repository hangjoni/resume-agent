import streamlit as st
import auth_functions
from io import StringIO
import pymupdf
import requests

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
        pdf = pymupdf.open(stream=content, filetype="pdf")
        text = ""
        for page in pdf:
            text += page.get_text()
        pdf.close()
            # display pdf file as text
        st.write(text)

        # make a request to the server
        # add a spinner while waiting for response
        st.header("Server response:")
        with st.spinner('Waiting for server response...'):
            # make a post request using query text

            response = requests.post(st.secrets["SERVER_URL"]+ "/parse_resume_text", params={"text": text})
        
        st.write(response.json())

        # # To convert to a string based IO:
        # stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        # st.write(stringio)

        # # To read file as string:
        # string_data = stringio.read()
        # st.write(string_data)
