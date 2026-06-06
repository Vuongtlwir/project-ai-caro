import time

from src.game.constants import TIME_LIMIT


class Timer:
    """Đồng hồ bấm giờ cho vòng tìm kiếm của AI."""

    def __init__(self, limit_sec: float = TIME_LIMIT):
        # giới hạn thời gian (giây) cho một lượt tìm kiếm
        self.limit_sec = limit_sec
        self._start: float = 0.0
        self._expired: bool = False

    # ----------------------------------------
    # Điều khiển
    # ----------------------------------------

    def start(self) -> None:
        """Bắt đầu đếm giờ cho lượt tìm kiếm mới."""
        self._start = time.perf_counter()
        self._expired = False

    def reset(self) -> None:
        """Đặt lại về trạng thái ban đầu."""
        self._start = 0.0
        self._expired = False

    # ----------------------------------------
    # Truy vấn thời gian
    # ----------------------------------------

    def is_up(self) -> bool:
        """Trả về True nếu đã dùng hết thời gian cho phép."""
        if self._expired:
            return True
        # cache kết quả vào _expired để tránh gọi perf_counter liên tục
        if (time.perf_counter() - self._start) >= self.limit_sec:
            self._expired = True
            return True
        return False

    def elapsed(self) -> float:
        """Thời gian đã trôi qua (giây) kể từ start()."""
        return time.perf_counter() - self._start

    def remaining(self) -> float:
        """Thời gian còn lại (giây); không nhỏ hơn 0."""
        return max(0.0, self.limit_sec - self.elapsed())
