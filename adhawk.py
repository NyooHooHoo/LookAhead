import adhawkapi
import adhawkapi.frontend
import Log


class EyeTracker:
    def __init__(self):
        pass
        # connect to proper glasses
    def start(self):
        print("EHLLO")
        self.api = adhawkapi.frontend.FrontendApi(ble_device_name='ADHAWK MINDLINK-303')

        # track events and that
        self.api.register_stream_handler(adhawkapi.PacketType.EYETRACKING_STREAM, self.handle_eye_data)
        self.api.register_stream_handler(adhawkapi.PacketType.EVENTS, self.handle_eye_events)

        # handle connecting and disconnecting properly
        self.api.start(tracker_connect_cb=self.handle_connect, tracker_disconnect_cb=self.handle_disconnect)
        
    def shutdown(self):
        self.api.shutdown()

    @staticmethod
    def handle_eye_data(et_data: adhawkapi.EyeTrackingStreamData):
        if et_data.gaze is not None:
            xvec, yvec, zvec, vergence = et_data.gaze
            print(f'Gaze={xvec:.2f},y={yvec:.2f},z={zvec:.2f},vergence={vergence:.2f}')

        if et_data.eye_center is not None:
            if et_data.eye_mask == adhawkapi.EyeMask.BINOCULAR:
                rxvec, ryvec, rzvec, lxvec, lyvec, lzvec = et_data.eye_center
                print(f'Eye center: Left=(x={lxvec:.2f},y={lyvec:.2f},z={lzvec:.2f}) '
                      f'Right=(x={rxvec:.2f},y={ryvec:.2f},z={rzvec:.2f})')

        if et_data.pupil_diameter is not None:
            if et_data.eye_mask == adhawkapi.EyeMask.BINOCULAR:
                rdiameter, ldiameter = et_data.pupil_diameter
                print(f'Pupil diameter: Left={ldiameter:.2f} Right={rdiameter:.2f}')

        if et_data.imu_quaternion is not None:
            if et_data.eye_mask == adhawkapi.EyeMask.BINOCULAR:
                x, y, z, w = et_data.imu_quaternion
                print(f'IMU: x={x:.2f},y={y:.2f},z={z:.2f},w={w:.2f}')

    @staticmethod
    def handle_eye_events(event_type, timestamp, *args):
        if event_type == adhawkapi.Events.BLINK:
            duration = args[0]
            print(f'Got blink: {timestamp} {duration}')
        if event_type == adhawkapi.Events.EYE_CLOSED:
            eye_idx = args[0]
            print(f'Eye Close: {timestamp} {eye_idx}')
        if event_type == adhawkapi.Events.EYE_OPENED:
            eye_idx = args[0]
            print(f'Eye Open: {timestamp} {eye_idx}')

    def handle_connect(self):
        Log.info("tracker connected")
        self.api.set_et_stream_rate(60, callback=lambda *args: None)

        self.api.set_et_stream_control([
            adhawkapi.EyeTrackingStreamTypes.GAZE,
            adhawkapi.EyeTrackingStreamTypes.EYE_CENTER,
            adhawkapi.EyeTrackingStreamTypes.PUPIL_DIAMETER,
            adhawkapi.EyeTrackingStreamTypes.IMU_QUATERNION,
        ], True, callback=lambda *args: None)

        self.api.set_event_control(adhawkapi.EventControlBit.BLINK, 1, callback=lambda *args: None)
        self.api.set_event_control(adhawkapi.EventControlBit.EYE_CLOSE_OPEN, 1, callback=lambda *args: None)

    def handle_disconnect(self):
        Log.info("tracker disconnected")


if __name__ == "__main__":
    eyetracker = EyeTracker()
    try:
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        eyetracker.shutdown()

