from api.chargers.services import save_chargers_to_db


def sincronize_data_with_API_chargers_cron():
    print("SINCRONITZANT CHARGERS CRON")
    save_chargers_to_db()