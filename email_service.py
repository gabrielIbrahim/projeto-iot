import yagmail

#EMAIL = "ibrahimmartinsimperio@gmail.com"
#APP_PASSWORD = "iidv xdix sxvs hlgr"
#DESTINO = "ibrahimmartinsimperio@gmail.com"

def send_alert_email(message):
    try:
        yag = yagmail.SMTP(EMAIL, APP_PASSWORD)

        yag.send(
            to=DESTINO,
            subject="🚨 Alerta IoT",
            contents=message
        )

        print("Email enviado com sucesso!")

    except Exception as e:
        print("Erro ao enviar email:", e)
