import reflex as rx
from todo_app.auth.state import AuthState

def auth_page():
    return rx.center(
        rx.vstack(
            rx.heading(
                rx.cond(AuthState.is_login, "Sign In", "Create Account",),
                size="8",
                color_scheme='sky'
            ),
            rx.form(
                rx.vstack(
                    rx.input(placeholder="Username", name="username", is_required=True, width="100%"),
                    rx.input(placeholder="Password", type="password", name="password", is_required=True, width="100%"),
                    rx.cond(
                        rx.input(placeholder="Confirm Password", type="password", name="confirm_password", width="100%")
                    ),
                    rx.button(
                        rx.cond(AuthState.is_login, "Login", "Sign Up"),
                        type="submit",
                        width="100%",
                        color_scheme="blue",
                        loading=AuthState.is_loading,
                    ),
                    spacing="4",
                    width="100%",
                ),
                on_submit=AuthState.handle_submit,
                width="320px",
            ),
            rx.box(
                rx.text(rx.cond(AuthState.is_login, "Don't have an account?", "Already have an account?"), size="2"),
                rx.link(
                    rx.cond(AuthState.is_login, " Sign Up", " Log In"),
                    on_click=AuthState.toggle_auth_mode,
                    color_scheme="blue",
                    cursor="pointer",
                    size="2",
                ),
                spacing="2",
                margin_top="1em",
            ),
            padding="2.5em",
            border="1px solid #EAEAEA",
            border_radius="15px",
            bg="white",
        ),
        height="100vh",
        bg="#1E224E",
    )
