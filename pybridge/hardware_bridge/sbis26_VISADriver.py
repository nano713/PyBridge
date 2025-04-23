import time
import pyvisa
# logger = set_logger(get_module_name(__file__))

class SBIS26VISADriver:
    """VISA class driver for the OptoSigma stage SBIS26."""

    def __init__(self, rsrc_name):
        self._stage = None
        self.rsrc_name = rsrc_name
        self.speed_ini = [-1, -1, -1]
        self.speed_fin = [-1, -1, -1]
        self.accel_t = [-1, -1, -1]
        self.position = [0, 0, 0]

    def connect(self):
        """Initializes the stage."""
        rm = pyvisa.ResourceManager()
        self._stage = rm.open_resource(self.rsrc_name)
        self._stage.baud_rate = 38400
        self._stage.data_bits = 8
        self._stage.parity = pyvisa.constants.Parity.none
        self._stage.stop_bits = pyvisa.constants.StopBits.one
        self._stage.flow_control.rts_cts = False #check documentation if true 
        self._stage.read_termination = '\r\n'
        # self._stage.write_termination = '\n'
        self._stage.query("*IDN?")
        self._stage.query("#CONNECT:")

    def check_error(self, channel):
        """Gets the status of the stage.
        Args:
            channel (int): Channel of the stage.
        Returns (str): Status of the stage.
        """
        status = {"C": "Stopped by clockwise limit sensor detected.",
                  "W": "Stopped by counterclockwise limit sensor detected.",
                  "E": "Stopped by both of limit sensor.",
                  "K": "Normal"}

        while True:
            self._stage.query(f"SRQ:D,{channel}")
            error_str = self._stage.query(f"SRQ:D,{channel}")
            key = error_str.split(",")[3]
            if error_str in status.keys():
                channel_val = int(error_str.split(",")[1])
                if channel_val == channel:
                    return error_str[key]
                else:
                    continue
            time.sleep(0.2)

    def status(self, channel):
        """Gets the status of the stage.
        Args:
            channel (int): Channel of the stage.
        Returns (str): Status of the stage.
        """
        self._stage.query(f"SRQ:D,{channel}")
        status_str = self._stage.query(f"SRQ:D,{channel}")
        key = status_str.split(",")[-1]
        return key

    def get_position(self, channel):
        """Gets the position of the stage.
        Args:
            channel (int): Channel of the stage.
        Returns (float): Position of the stage.
        """
        while IndexError
        return int(self._stage.query(f"Q:D,{channel}").split(",")[2])

    def move(self, position, channel):
        """Moves the stage to the specified position.
        Args:
            position (int): Position to move the stage to.
            channel (int): Channel of the stage.

         """
        if position >= 0:
            self._stage.query(f"A:D,{channel},+{position}")
        else:
            self._stage.query(f"A:D,{channel},{position}")
        self.wait_for_ready(channel)
        self.position[channel - 1] = position

    def move_relative(self, position, channel):
        """Moves the stage to the specified relative position.
        Args:
            position (int): Relative position to move the stage to.
            channel (int): Channel of the stage.
        """

        self._stage.query(f"M:D,{channel},{position}")
        self.wait_for_ready(channel)
        self.position[channel - 1] = self.position[channel - 1] + position

    def set_speed(self, speed_ini, speed_fin, accel_t, channel):
        """Sets the speed of the stage.
        Args:
            speed_ini (int): Initial speed of the stage.
            speed_fin (int): Final speed of the stage.
            accel_t (int): Acceleration time of the stage.
            channel (int): Channel of the stage.
        """
        self.speed_ini[channel - 1] = speed_ini
        self.speed_fin[channel - 1] = speed_fin
        self.accel_t[channel - 1] = accel_t
        if 0 < speed_ini <= speed_fin and accel_t > 0:
            self._stage.query(f"D:D,{channel},{speed_ini},{speed_fin},{accel_t}")
        else:
            logger.error("Invalid parameters")

    def get_speed(self, channel):
        """Gets the speed of the stage."""
        if (self.speed_ini[channel - 1] is None or self.speed_fin[channel - 1] is None or self.accel_t[channel - 1] is None):
            return logger.error("Parameters are None.")
        return self.speed_ini[channel - 1], self.speed_fin[channel - 1], self.accel_t[channel - 1]

    def stop(self):
        """Stops the stage."""
        self._stage.query("LE:A")

    def wait_for_ready(self, channel):
        """Waits for the stage to be ready."""

        time0 = time.time()
        while self.status(channel) != "R":
            logger.debug(self.status(channel))
            time1 = time.time() - time0
            if time1 >= 60:
                logger.error("Timeout")
                break
            time.sleep(0.2)

    def home(self, channel):
        """ Sends the stage to the home position."""
        self._stage.query(f"H:D,{channel}")
        self.wait_for_ready(channel)
        self.position[channel - 1] = 0

    def close(self):
        """Closes the stage."""
        pyvisa.ResourceManager().close()