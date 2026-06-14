import logging

logging.basicConfig(
    filename='tournament_app.log',
    level=logging.INFO,
    format='[%(asctime)s] - [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

matches = [
    {
        "match_id": "M01",
        "team_a": "T1",
        "team_b": "GenG",
        "score_a": 2,
        "score_b": 1,
        "status": "Completed"
    },
    {
        "match_id": "M02",
        "team_a": "JDG",
        "team_b": "BLG",
        "score_a": 0,
        "score_b": 0,
        "status": "Pending"
    }
]

def display_matches(match_list):
    logger.info("User viewed the match list.")
    
    if not match_list:
        print("Hiện chưa có trận đấu nào trong hệ thống.")
        return

    print("\n--- LỊCH THI ĐẤU & KẾT QUẢ ---")
    print(f"{'Mã trận':<10}| {'Đội A':<15}| {'Đội B':<15}| {'Tỷ số':<8}| {'Trạng thái'}")
    print("-" * 68)
    
    for match in match_list:
        try:
            m_id = match['match_id']
            ta = match['team_a']
            tb = match['team_b']
            sa = match['score_a']
            sb = match['score_b']
            status = match['status']
            print(f"{m_id:<10}| {ta:<15}| {tb:<15}| {sa}-{sb:<6}| {status}")
        except KeyError as e:
            logger.error(f"Missing data key in match dictionary: {e}")
            print(f"Lỗi: Thiếu dữ liệu trận đấu (KeyError: {e})")

def add_match(match_list):
    print("\n--- THÊM TRẬN ĐẤU MỚI ---")
    match_id = input("Nhập mã trận đấu: ").strip()
    
    if not match_id:
        print("\nMã trận đấu không được để trống.")
        logger.warning("User tried to add a match with empty match ID.")
        return

    if any(m.get('match_id') == match_id for m in match_list):
        print(f"\nLỗi: Mã trận đấu {match_id} đã tồn tại.")
        logger.warning(f"Match ID {match_id} already exists.")
        return

    team_a = input("Nhập tên Đội A: ").strip()
    team_b = input("Nhập tên Đội B: ").strip()

    if not team_a or not team_b:
        print("\nTên đội không được để trống.")
        logger.warning("User tried to add a match with empty team name.")
        return

    new_match = {
        "match_id": match_id,
        "team_a": team_a,
        "team_b": team_b,
        "score_a": 0,
        "score_b": 0,
        "status": "Pending"
    }
    match_list.append(new_match)
    print(f"\nThành công: Đã thêm trận đấu {match_id}.")
    logger.info(f"Match {match_id} added successfully")

def update_score(match_list):
    print("\n--- CẬP NHẬT TỶ SỐ TRẬN ĐẤU ---")
    match_id = input("Nhập mã trận đấu cần cập nhật: ").strip()
    
    target_match = next((m for m in match_list if m.get('match_id') == match_id), None)
    
    if not target_match:
        print(f"\nKhông tìm thấy trận đấu mang mã {match_id}.")
        logger.warning(f"User tried to update non-existing match {match_id}")
        return

    try:
        print(f"\nTrận đấu: {target_match['team_a']} vs {target_match['team_b']} ({target_match['status']})")
        
        while True:
            try:
                score_a_str = input(f"Nhập điểm Đội A: ")
                score_a = int(score_a_str)
                if score_a < 0:
                    print("\nĐiểm số phải lớn hơn hoặc bằng 0.")
                    logger.error(f"Negative score input detected: {score_a}")
                    continue
                break
            except ValueError as e:
                print("\nĐiểm số phải là số nguyên. Vui lòng nhập lại.")
                logger.error(f"Invalid score input. Error: {e}")

        while True:
            try:
                score_b_str = input(f"Nhập điểm Đội B: ")
                score_b = int(score_b_str)
                if score_b < 0:
                    print("\nĐiểm số phải lớn hơn hoặc bằng 0.")
                    logger.error(f"Negative score input detected: {score_b}")
                    continue
                break
            except ValueError as e:
                print("\nĐiểm số phải là số nguyên. Vui lòng nhập lại.")
                logger.error(f"Invalid score input. Error: {e}")

        status = "Pending"
        if score_a > 0 or score_b > 0:
            status = "Completed"
        else:
            confirm = input("\nTỷ số đang là 0-0. Trọng tài có xác nhận trận đã hoàn thành không? (y/n): ").strip().lower()
            if confirm == 'y':
                status = "Completed"

        target_match['score_a'] = score_a
        target_match['score_b'] = score_b
        target_match['status'] = status

        print(f"\nThành công: Đã cập nhật tỷ số trận đấu {match_id}.")
        logger.info(f"Match {match_id} score updated successfully")

    except KeyError as e:
        logger.error(f"Data corruption in match {match_id}. Missing key: {e}")
        print("\nLỗi hệ thống: Dữ liệu trận đấu bị thiếu cấu trúc chuẩn.")

def determine_winner(match):
    try:
        if match.get("status") == "Pending":
            return "Not Started"
        
        if match["score_a"] > match["score_b"]:
            return match["team_a"]
        elif match["score_b"] > match["score_a"]:
            return match["team_b"]
        else:
            return "Draw"
    except KeyError as e:
        logger.error(f"Missing keys for determining winner: {e}")
        return "Data Error"

def generate_report(match_list):
    logger.info("User generated tournament report.")
    print("\n--- BÁO CÁO THỐNG KÊ GIẢI ĐẤU ---")
    
    completed_matches = [m for m in match_list if m.get("status") == "Completed"]
    
    if not completed_matches:
        print("Chưa có trận đấu nào hoàn thành.")
        print("Tổng số trận đã hoàn thành: 0")
        return

    for match in completed_matches:
        try:
            m_id = match['match_id']
            ta = match['team_a']
            tb = match['team_b']
            sa = match['score_a']
            sb = match['score_b']
            winner = determine_winner(match)
            print(f"{m_id}: {ta} {sa}-{sb} {tb} | Kết quả: {winner}")
        except KeyError as e:
            logger.error(f"Report generation error, missing key: {e}")
            
    print(f"\nTổng số trận đã hoàn thành: {len(completed_matches)}")

def main():
    while True:
        print("\n===== HỆ THỐNG QUẢN LÝ GIẢI ĐẤU RIKKEI ESPORTS =====")
        print("1. Hiển thị lịch thi đấu & Kết quả")
        print("2. Thêm trận đấu mới")
        print("3. Cập nhật tỷ số trận đấu")
        print("4. Báo cáo thống kê")
        print("5. Thoát chương trình")
        print("==================================================")
        
        choice = input("Chọn chức năng (1-5): ").strip()

        if choice == '1':
            display_matches(matches)
        elif choice == '2':
            add_match(matches)
        elif choice == '3':
            update_score(matches)
        elif choice == '4':
            generate_report(matches)
        elif choice == '5':
            print("Đang đóng hệ thống... Tạm biệt!")
            logger.info("System closed and program exited.")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng nhập từ 1 đến 5.")
            logger.warning("Invalid menu choice selected")

if __name__ == "__main__":
    main()