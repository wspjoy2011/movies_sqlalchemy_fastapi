REGISTRATION_HTML_CONTENT = """
<html>
<head></head>
<body>
    <div style="border: 1px solid #ddd; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); padding: 20px; max-width: 400px; margin: 20px auto; font-family: 'Arial', sans-serif; background-color: #f9f9f9;">
        <h2 style="color: #007BFF; text-align: center; margin-top: 0;">Welcome to Our Platform</h2>
        <p style="margin: 10px 0; line-height: 1.5;">Dear {fullname},</p>
        <p style="margin: 10px 0; line-height: 1.5;">Thank you for registering! To complete your registration, please use the activation token below:</p>
        <p style="font-size: 24px; font-weight: bold; background-color: #FFEB3B; text-align: center; padding: 10px; border-radius: 4px; margin: 20px 0; word-break: break-all;">{activation_link}</p>
        <p style="margin: 10px 0; line-height: 1.5;">Regards,</p>
        <p style="margin: 10px 0; line-height: 1.5; font-style: italic;">The Mate team</p>
    </div>
</body>
</html>
"""
