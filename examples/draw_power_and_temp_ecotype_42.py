import requests
import matplotlib.pyplot as plt
import arrow
import matplotlib.dates as mdate


def main():
    SERVER_NAME = "ecotype-42"

    START_DATE = "2019-04-12T10:00:00"
    END_DATE = "2019-04-12T11:00:00"

    start_epoch = arrow.get(START_DATE).timestamp
    end_epoch = arrow.get(END_DATE).timestamp

    sensors = requests.get("https://api.seduce.fr/servers/all/sensors").json()
    [server_sensors] = [sensor for sensor in sensors if sensor.get("name") == SERVER_NAME]

    front_temperature = requests.get(f"https://api.seduce.fr/sensors/{server_sensors.get('temp').get('front')}/measurements?start_date={start_epoch}&end_date={end_epoch}").json()
    back_temperature = requests.get(f"https://api.seduce.fr/sensors/{server_sensors.get('temp').get('back')}/measurements?start_date={start_epoch}&end_date={end_epoch}").json()
    power_consumption_pdu1 = requests.get(f"https://api.seduce.fr/sensors/{server_sensors.get('power')[0]}/measurements?start_date={start_epoch}&end_date={end_epoch}").json()
    power_consumption_pdu2 = requests.get(f"https://api.seduce.fr/sensors/{server_sensors.get('power')[1]}/measurements?start_date={start_epoch}&end_date={end_epoch}").json()

    fig = plt.figure()

    ax = plt.axes()
    ax2 = ax.twinx()

    ax.plot(mdate.epoch2num(front_temperature.get("epoch_ts")), front_temperature.get("values"), color='blue', label='temp (cold aisle)', linewidth=0.5)
    ax.plot(mdate.epoch2num(back_temperature.get("epoch_ts")), back_temperature.get("values"), color='red', label='temp (hot aisle)', alpha=0.5, linewidth=0.5)

    ax2.plot(mdate.epoch2num(power_consumption_pdu1.get("epoch_ts")), power_consumption_pdu1.get("values"), color='green', label='power (pdu1)', linewidth=0.5)
    ax2.plot(mdate.epoch2num(power_consumption_pdu2.get("epoch_ts")), power_consumption_pdu2.get("values"), color='orange', label='power (pdu2)', linewidth=0.5)

    ax.xaxis_date()

    # Define the format of the date displayed on the x axis
    date_fmt = '%d-%m-%y %H:%M:%S'

    # Use a DateFormatter to set the data to the correct format.
    date_formatter = mdate.DateFormatter(date_fmt)
    ax.xaxis.set_major_formatter(date_formatter)

    # Make space for and rotate the x-axis tick labels
    fig.autofmt_xdate()

    ax.legend(loc="upper left", ncol=1, frameon=True)
    ax2.legend(loc="upper right", ncol=1, frameon=True)

    ax.set_ylim([0, 45])
    ax2.set_ylim([-30, 200])

    plt.title(f"Power consumptions and temperatures of {SERVER_NAME}")

    ax.set_xlabel('Time')
    ax.set_ylabel("Temperature (deg. C)")
    ax2.set_ylabel("Power consumption (W)")

    plt.show()


if __name__ == "__main__":
    main()
