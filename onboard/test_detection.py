import cv2

from perception.camera import Camera
from perception.detector import TargetDetector


def main():
    print("[TEST] test_detection başladı")

    camera = Camera(device=0, width=640, height=480)
    print("[TEST] Kamera açıldı")

    detector = TargetDetector(min_area=500)
    print("[TEST] Detector hazır")

    try:
        while True:
            frame = camera.get_frame()

            if frame is None:
                print("[TEST] Frame alınamadı")
                continue

            print("[TEST] Frame alındı")

            result = detector.detect(frame)

            if result is not None:
                x, y, w, h = result["bbox"]
                cx = int(result["cx"])
                cy = int(result["cy"])

                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.circle(frame, (cx, cy), 5, (255, 0, 0), -1)

                text = (
                    f"Target area={result['area']:.0f} "
                    f"err_x={result['error_x']:.1f} "
                    f"err_y={result['error_y']:.1f}"
                )
                cv2.putText(
                    frame,
                    text,
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2,
                )

                print(
                    f"[DETECT] cx={result['cx']:.1f}, cy={result['cy']:.1f}, "
                    f"err_x={result['error_x']:.1f}, err_y={result['error_y']:.1f}, "
                    f"area={result['area']:.1f}"
                )

            cv2.imshow("Detection", frame)

            if result is not None:
                cv2.imshow("Mask", result["mask"])

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                print("[TEST] q basıldı, çıkılıyor")
                break

    finally:
        print("[TEST] Kaynaklar kapatılıyor")
        camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()