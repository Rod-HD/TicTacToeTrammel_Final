import collections
import logging
import math
import random
import time
from typing import Dict, List, Optional, Tuple

from board import Board

# Định nghĩa DEFAULT_TIME_LIMIT trực tiếp trong minimax.py
DEFAULT_TIME_LIMIT = 2.0 # Giới hạn thời gian mặc định cho AI (ví dụ: 2 giây)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class MinimaxAI:
    """
    AI cho cờ Caro: easy = Q-learning; hard = Minimax tối ưu với chặn sát khi (win_len - 1) hoặc (win_len - 2).
    """

    def __init__(self, difficulty: str = "medium"):
        self.difficulty = difficulty
        self.board = Board()  # Sample board để lấy cấu hình
        # max_depth_hard sẽ được thiết lập dựa trên kích thước bàn cờ
        self.max_depth_hard = self._get_dynamic_max_depth()
        # Độ sâu cố định cho chế độ medium, giảm tối đa để nhanh nhất
        self.max_depth_medium = 1 # Đã điều chỉnh để cực kỳ nhanh.
        self.transposition_table: Dict[str, float] = {}
        
        # Khởi tạo bảng Zobrist
        self.zobrist_keys = {}
        for i in range(self.board.rows):
            for j in range(self.board.cols):
                # Các ký hiệu có thể xuất hiện trên bảng (EMPTY, OBSTACLE, X, O)
                for symbol in [self.board.EMPTY, self.board.OBSTACLE, 'X', 'O']:
                    # Sửa lỗi: random.getandbits(64) -> random.getrandbits(64)
                    self.zobrist_keys[(i, j, symbol)] = random.getrandbits(64)
        
        logger.debug(f"Initialized MinimaxAI with difficulty: {difficulty}, dynamic max_depth for hard: {self.max_depth_hard}, fixed max_depth for medium: {self.max_depth_medium}")

        # Q-table dùng cho difficulty "easy"
        self.q_table = collections.defaultdict(
            lambda: [0.0] * (self.board.rows * self.board.cols) # Kích thước bảng Q phụ thuộc vào số ô
        )
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.exploration_rate = 0.2
        self.last_state = None
        self.last_action = None

    def _get_dynamic_max_depth(self) -> int:
        """
        Điều chỉnh độ sâu tìm kiếm động dựa trên kích thước bàn cờ.
        Bàn cờ càng lớn, độ sâu càng nhỏ để giữ tốc độ.
        """
        board_area = self.board.rows * self.board.cols
        if board_area <= 25:  # Ví dụ 5x5, win_len 4
            return 8  # Độ sâu này thường mang lại sức mạnh tốt mà vẫn nhanh
        elif board_area <= 49: # Ví dụ 7x7
            return 6
        elif board_area <= 100: # Ví dụ 10x10
            return 4
        else: # Bàn cờ lớn hơn nhiều
            return 3 # Giảm độ sâu để tránh quá tải

    def best(self, board: Board, ai_symbol: str, human_symbol: str) -> Tuple[int, int]:
        """
        Xác định nước đi tốt nhất dựa trên độ khó đã chọn, sử dụng IDDFS cho chế độ "hard",
        Minimax với độ sâu cố định cho chế độ "medium", và Q-learning cho "easy".
        """
        self.board = board # Cập nhật board hiện tại cho AI

        if self.difficulty == "easy":
            state = self._get_state_representation(board)
            legal_moves = list(board.get_legal_moves())
            if not legal_moves:
                return (0, 0) # Không có nước đi nào khả dụng

            chosen_move = None # Đảm bảo biến chosen_move được khởi tạo

            if random.uniform(0, 1) < self.exploration_rate:
                # Khám phá: chọn một nước đi ngẫu nhiên
                chosen_move = random.choice(legal_moves)
            else:
                # Khai thác: chọn nước đi tốt nhất từ Q-table
                best_score = -math.inf
                move_options = []

                for r, c in legal_moves:
                    idx = r * board.cols + c
                    if idx < len(self.q_table[state]): # Kiểm tra giới hạn để tránh lỗi
                        score = self.q_table[state][idx]
                        if score > best_score:
                            best_score = score
                            chosen_move = (r, c) # Gán giá trị vào chosen_move
                            move_options = [(r, c)]
                        elif score == best_score:
                            move_options.append((r, c))
                
                if move_options:
                    chosen_move = random.choice(move_options) # Gán giá trị vào chosen_move
                else: # Fallback nếu không có nước đi nào có điểm số tốt, chọn ngẫu nhiên
                    chosen_move = random.choice(legal_moves) # Gán giá trị vào chosen_move

            self.last_state = state
            self.last_action = chosen_move # Sử dụng biến đã được gán giá trị
            return chosen_move

        elif self.difficulty == "medium":
            logger.debug(f"Starting Minimax search for 'medium' difficulty at fixed depth: {self.max_depth_medium}")
            start_time = time.time()
            legal_moves = list(board.get_legal_moves())
            if not legal_moves:
                return (0, 0) # Không có nước đi nào khả dụng

            best_value = -math.inf
            best_move = legal_moves[0] # Khởi tạo với một nước đi hợp lệ
            
            # Sắp xếp nước đi cho chế độ medium để có hiệu suất tốt hơn
            # Đây là yếu tố chính giúp nó giỏi hơn easy mà vẫn nhanh
            moves_to_consider = self._get_ordered_moves(board, ai_symbol, human_symbol)
            if not moves_to_consider: # Fallback nếu không có nước đi nào sau khi sắp xếp
                return (0, 0)
            
            # Với depth=1, ta chỉ cần lặp qua các nước đi hợp lệ và đánh giá chúng trực tiếp.
            # Không cần gọi đệ quy _minimax nữa, giúp nhanh hơn rất nhiều.
            for r, c in moves_to_consider:
                board.place(r, c, ai_symbol)
                value = self._evaluate_board(board, ai_symbol, human_symbol)
                board.undo_last_move()

                if value > best_value:
                    best_value = value
                    best_move = (r, c)
            
            end_time = time.time()
            logger.debug(f"Minimax search for 'medium' took {end_time - start_time:.4f} seconds. Final move: {best_move}")
            return best_move

        elif self.difficulty == "hard":
            start_time = time.time()
            legal_moves = list(board.get_legal_moves())
            if not legal_moves:
                return (0, 0) # Không có nước đi nào khả dụng
            
            best_move_so_far = legal_moves[0] 
            best_score_so_far = -math.inf

            # Xóa bảng chuyển vị cho mỗi lần tìm kiếm mới
            self.transposition_table.clear() 

            # IDDFS: Tăng dần độ sâu cho đến khi hết thời gian
            for current_depth in range(1, self.max_depth_hard + 1):
                logger.debug(f"Starting IDDFS search at depth: {current_depth}")
                try:
                    # Gọi Minimax với giới hạn thời gian
                    score, move = self._minimax_id(
                        board, current_depth, True, -math.inf, math.inf,
                        ai_symbol, human_symbol, start_time, DEFAULT_TIME_LIMIT
                    )

                    # Nếu AI tìm thấy nước thắng hoặc thua chắc chắn ở độ sâu hiện tại, dừng lại
                    if score == math.inf or score == -math.inf:
                        best_move_so_far = move if move is not None else best_move_so_far
                        best_score_so_far = score
                        logger.debug(f"Found winning/losing move at depth {current_depth}. Stopping IDDFS.")
                        break # Dừng IDDFS nếu tìm thấy nước thắng/thua

                    # Chỉ cập nhật nước đi tốt nhất nếu đã tìm thấy ở độ sâu hiện tại
                    # và điểm số tốt hơn hoặc bằng điểm số hiện tại
                    if move is not None and score > best_score_so_far:
                        best_score_so_far = score
                        best_move_so_far = move
                    
                    # Nếu không tìm thấy nước đi ở độ sâu hiện tại, hãy dùng nước đã tìm được
                    elif move is None and current_depth == 1:
                        pass

                    logger.debug(f"Finished depth {current_depth}. Best move so far: {best_move_so_far} with score: {best_score_so_far}")

                except TimeoutError:
                    logger.debug(f"Timeout at depth {current_depth}. Using best move found so far.")
                    break # Dừng IDDFS nếu hết thời gian

                # Kiểm tra thời gian sau mỗi lần hoàn thành một độ sâu
                if time.time() - start_time >= DEFAULT_TIME_LIMIT:
                    logger.debug(f"Time limit reached after depth {current_depth}. Using best move found so far.")
                    break
            
            end_time = time.time()
            logger.debug(f"Minimax IDDFS search took {end_time - start_time:.4f} seconds. Final move: {best_move_so_far}")
            
            return best_move_so_far
        else:
            logger.error(f"Unknown difficulty level: '{self.difficulty}'. Falling back to random move.")
            legal_moves = list(board.get_legal_moves())
            if legal_moves:
                return random.choice(legal_moves)
            return (0,0)

    def _minimax_id(self, board: Board, depth: int, maximizing_player: bool, alpha: float, beta: float,
                     ai_symbol: str, human_symbol: str, start_time: float, time_limit: float) -> Tuple[float, Optional[Tuple[int, int]]]:
        """
        Thuật toán Minimax với cắt tỉa Alpha-Beta, Transposition Table và giới hạn thời gian.
        Dùng cho chế độ 'hard'.
        """
        
        # Kiểm tra thời gian trước khi bắt đầu một nút mới trong cây tìm kiếm
        if time.time() - start_time >= time_limit:
            raise TimeoutError("Time limit exceeded")

        # Kiểm tra Transposition Table (Zobrist Hashing)
        state_key = self._calculate_zobrist_hash(board)
        if state_key in self.transposition_table:
            # Transposition table lưu giá trị của trạng thái, không lưu nước đi
            # Vì vậy, nếu trạng thái đã có, ta chỉ trả về giá trị đã tính toán
            # Nước đi (thứ hai trong tuple) sẽ là None vì chúng ta không lưu nó
            return self.transposition_table[state_key], None

        # Base cases: game over hoặc độ sâu đạt tới giới hạn
        if board.has_winner_any():
            winner_sym = board.get_winner_symbol()
            if winner_sym == ai_symbol:
                return math.inf, None # AI thắng
            elif winner_sym == human_symbol:
                return -math.inf, None # Người chơi thắng
        elif board.is_draw():
            return 0, None # Hòa
        
        if depth == 0:
            return self._evaluate_board(board, ai_symbol, human_symbol), None

        # Lấy các nước đi đã được sắp xếp
        moves_to_consider = self._get_ordered_moves(board, ai_symbol if maximizing_player else human_symbol,
                                                    human_symbol if maximizing_player else ai_symbol)

        if not moves_to_consider:
            return self._evaluate_board(board, ai_symbol, human_symbol), None

        best_value = -math.inf if maximizing_player else math.inf
        best_move = None

        for r, c in moves_to_consider:
            # Kiểm tra thời gian trước khi thực hiện nước đi
            if time.time() - start_time >= time_limit:
                raise TimeoutError("Time limit exceeded")

            board.place(r, c, ai_symbol if maximizing_player else human_symbol)
            
            try:
                # Đệ quy gọi _minimax_id
                value, _ = self._minimax_id(board, depth - 1, not maximizing_player, alpha, beta, ai_symbol, human_symbol, start_time, time_limit)
            except TimeoutError:
                board.undo_last_move() # Đảm bảo hoàn tác nếu có timeout
                raise # Ném lại ngoại lệ để dừng tìm kiếm

            board.undo_last_move() # Hoàn tác nước đi

            if maximizing_player:
                if value > best_value:
                    best_value = value
                    best_move = (r, c)
                alpha = max(alpha, best_value)
            else: # minimizing_player
                if value < best_value:
                    best_value = value
                    best_move = (r, c)
                beta = min(beta, best_value)

            # Alpha-Beta Pruning
            if beta <= alpha:
                break
        
        self.transposition_table[state_key] = best_value
        return best_value, best_move

    def _get_ordered_moves(self, board: Board, player_symbol: str, opponent_symbol: str) -> List[Tuple[int, int]]:
        """
        Sắp xếp các nước đi tiềm năng để tối ưu hóa cắt tỉa Alpha-Beta.
        Ưu tiên: Nước thắng > Nước chặn thắng > Nước tạo chuỗi mở của mình (win_len - 1)
        > Nước chặn chuỗi mở của đối thủ (win_len - 1) > Các nước đi tạo thế mạnh khác.
        """
        legal_moves = list(board.get_legal_moves())
        
        # 1. Ưu tiên các nước đi thắng ngay
        winning_moves = []
        for r, c in legal_moves:
            board.place(r, c, player_symbol)
            if board.has_winner(r, c, player_symbol):
                winning_moves.append((r, c))
            board.undo_last_move()
        if winning_moves:
            return winning_moves

        # 2. Ưu tiên các nước đi chặn thắng của đối thủ
        blocking_moves = []
        for r, c in legal_moves:
            board.place(r, c, opponent_symbol) # Giả sử đối thủ đi
            if board.has_winner(r, c, opponent_symbol):
                blocking_moves.append((r, c))
            board.undo_last_move()
        if blocking_moves:
            return blocking_moves

        # 3. Ưu tiên tạo chuỗi mở (win_len - 1) của mình (tấn công)
        # và chặn chuỗi mở (win_len - 1) của đối thủ (phòng thủ chủ động)
        high_priority_moves = []
        for r, c in legal_moves:
            # Kiểm tra tạo chuỗi mở của mình
            board.place(r, c, player_symbol)
            if self._is_creating_open_sequence(board, player_symbol, (r,c), board._win_len - 1):
                high_priority_moves.append((r, c))
            board.undo_last_move()
        
        # Sau đó kiểm tra chặn chuỗi mở của đối thủ
        for r, c in legal_moves:
            board.place(r, c, opponent_symbol) # Giả sử đối thủ đi
            if self._is_creating_open_sequence(board, opponent_symbol, (r,c), board._win_len - 1):
                # Nước này sẽ được AI chặn lại, nên ta thêm vào high_priority_moves cho player_symbol
                if (r,c) not in high_priority_moves: # Tránh trùng lặp
                    high_priority_moves.append((r, c))
            board.undo_last_move()

        if high_priority_moves:
            random.shuffle(high_priority_moves)
            return high_priority_moves

        # 4. Đánh giá các nước đi còn lại bằng heuristic
        scored_moves = []
        remaining_moves = [move for move in legal_moves if move not in winning_moves and move not in blocking_moves and move not in high_priority_moves]

        for r, c in remaining_moves:
            board.place(r, c, player_symbol)
            score = self._evaluate_board_for_ordering(board, player_symbol, opponent_symbol)
            board.undo_last_move()
            scored_moves.append((score, (r, c)))

        # Sắp xếp các nước đi giảm dần theo điểm số heuristic
        scored_moves.sort(key=lambda x: x[0], reverse=True)

        # Kết hợp tất cả các loại nước đi
        ordered_moves = []
        ordered_moves.extend(winning_moves)
        ordered_moves.extend(blocking_moves)
        ordered_moves.extend(high_priority_moves)
        ordered_moves.extend([move for score, move in scored_moves])
                
        return ordered_moves

    def _is_creating_open_sequence(self, board: Board, symbol: str, move: Tuple[int, int], length: int) -> bool:
        """
        Kiểm tra xem việc đặt quân tại 'move' có tạo ra một chuỗi 'length' mở hai đầu hay không.
        """
        r_move, c_move = move
        rows, cols = board.rows, board.cols
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)] # Ngang, dọc, chéo chính, chéo phụ

        for dr, dc in directions:
            current_len = 0
            open_ends = 0

            # Kiểm tra về một phía
            for k in range(length):
                cur_r, cur_c = r_move + k * dr, c_move + k * dc
                if not (0 <= cur_r < rows and 0 <= cur_c < cols and board._grid[cur_r][cur_c] == symbol):
                    break
                current_len += 1
            
            # Nếu chuỗi đạt được độ dài mong muốn từ điểm đặt quân theo một hướng
            if current_len == length:
                # Kiểm tra đầu còn lại của chuỗi
                # Điểm trước chuỗi (ngược hướng)
                prev_r, prev_c = r_move - dr, c_move - dc
                if 0 <= prev_r < rows and 0 <= prev_c < cols and board._grid[prev_r][prev_c] == board.EMPTY:
                    open_ends += 1
                
                # Điểm sau chuỗi (cùng hướng)
                next_r, next_c = r_move + length * dr, c_move + length * dc
                if 0 <= next_r < rows and 0 <= next_c < cols and board._grid[next_r][next_c] == board.EMPTY:
                    open_ends += 1
                
                if open_ends == 2:
                    return True # Chuỗi mở hai đầu

            # Reset current_len và kiểm tra theo hướng ngược lại
            current_len = 0
            open_ends = 0
            
            # Kiểm tra về phía ngược lại (quan trọng cho các chuỗi ở giữa)
            for k in range(length):
                cur_r, cur_c = r_move - k * dr, c_move - k * dc
                if not (0 <= cur_r < rows and 0 <= cur_c < cols and board._grid[cur_r][cur_c] == symbol):
                    break
                current_len += 1

            if current_len == length:
                # Kiểm tra đầu còn lại của chuỗi
                # Điểm sau chuỗi (ngược hướng với hướng kiểm tra hiện tại)
                next_r, next_c = r_move + dr, c_move + dc # Đây là đầu ban đầu của chuỗi nếu đi ngược lại
                if 0 <= next_r < rows and 0 <= next_c < cols and board._grid[next_r][next_c] == board.EMPTY:
                    open_ends += 1
                
                # Điểm trước chuỗi (cùng hướng với hướng kiểm tra hiện tại)
                prev_r, prev_c = r_move - length * dr, c_move - length * dc
                if 0 <= prev_r < rows and 0 <= prev_c < cols and board._grid[prev_r][prev_c] == board.EMPTY:
                    open_ends += 1
                
                if open_ends == 2:
                    return True # Chuỗi mở hai đầu

        return False

    def _evaluate_board_for_ordering(self, board: Board, player_sym: str, opponent_sym: str) -> float:
        """
        Hàm đánh giá rút gọn, chỉ tập trung vào việc tạo các chuỗi tiềm năng
        và kiểm soát trung tâm, dùng để sắp xếp nước đi.
        """
        score = 0
        for length in range(2, board._win_len + 1):
            score += self._count_sequences(board, player_sym, length) * (10**(length-1)) 
            score += self._count_open_sequences(board, player_sym, length) * (10**(length)) * 1.2

        for length in range(2, board._win_len + 1):
            score -= self._count_sequences(board, opponent_sym, length) * (10**(length-1)) * 1.8
            score -= self._count_open_sequences(board, opponent_sym, length) * (10**(length)) * 2.5

        center_row, center_col = board.rows // 2, board.cols // 2
        if board._grid[center_row][center_col] == board.EMPTY:
            score += 50

        return score

    def _evaluate_board(self, board: Board, ai_symbol: str, human_symbol: str) -> float:
        """
        Hàm đánh giá heuristic chính của AI. Đánh giá trạng thái bàn cờ hiện tại.
        """
        # Kiểm tra trạng thái thắng/thua ngay lập tức
        winner_sym = board.get_winner_symbol()
        if winner_sym == ai_symbol:
            return math.inf
        elif winner_sym == human_symbol:
            return -math.inf
        elif board.is_draw():
            return 0 # Hòa

        # Heuristic cho AI (tạo thế mạnh)
        ai_eval_score = 0
        ai_eval_score += self._count_open_sequences(board, ai_symbol, board._win_len - 1) * 1000000
        ai_eval_score += self._count_sequences(board, ai_symbol, board._win_len - 1) * 20000
        ai_eval_score += self._count_open_sequences(board, ai_symbol, board._win_len - 2) * 10000
        ai_eval_score += self._count_sequences(board, ai_symbol, board._win_len - 2) * 2000
        ai_eval_score += self._count_sequences(board, ai_symbol, 2) * 100
        ai_eval_score += self._count_sequences(board, ai_symbol, 3) * 400

        # Heuristic cho người chơi (phòng thủ), tăng cường hình phạt
        human_eval_score = 0
        human_eval_score += self._count_open_sequences(board, human_symbol, board._win_len - 1) * 2000000
        human_eval_score += self._count_sequences(board, human_symbol, board._win_len - 1) * 30000
        human_eval_score += self._count_open_sequences(board, human_symbol, board._win_len - 2) * 15000
        human_eval_score += self._count_sequences(board, human_symbol, board._win_len - 2) * 2500
        human_eval_score += self._count_sequences(board, human_symbol, 2) * 120
        human_eval_score += self._count_sequences(board, human_symbol, 3) * 500

        # Ưu tiên các ô ở trung tâm (thường là vị trí chiến lược)
        center_score = 0
        center_row, center_col = board.rows // 2, board.cols // 2
        
        if board._grid[center_row][center_col] == ai_symbol:
            center_score += 200
        elif board._grid[center_row][center_col] == human_symbol:
            center_score -= 250
        
        neighbors = [(r, c) for r in range(max(0, center_row-1), min(board.rows, center_row+2))
                             for c in range(max(0, center_col-1), min(board.cols, center_col+2))
                             if (r,c) != (center_row, center_col)]
        for r, c in neighbors:
            if board._grid[r][c] == ai_symbol:
                center_score += 40
            elif board._grid[r][c] == human_symbol:
                center_score -= 50

        score = ai_eval_score - human_eval_score + center_score
        return score

    def _count_sequences(self, board: Board, symbol: str, length: int) -> int:
        """
        Đếm số lượng chuỗi quân liên tiếp có độ dài 'length' của 'symbol'
        trên toàn bộ bàn cờ, không phân biệt chuỗi mở hay bị chặn.
        """
        count = 0
        rows, cols = board.rows, board.cols
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for r in range(rows):
            for c in range(cols):
                if board._grid[r][c] == symbol:
                    for dr, dc in directions:
                        prev_r, prev_c = r - dr, c - dc
                        if 0 <= prev_r < rows and 0 <= prev_c < cols and board._grid[prev_r][prev_c] == symbol:
                            continue

                        current_len = 0
                        for k in range(length):
                            cur_r, cur_c = r + k * dr, c + k * dc
                            if 0 <= cur_r < rows and 0 <= cur_c < cols and board._grid[cur_r][cur_c] == symbol:
                                current_len += 1
                            else:
                                break
                        if current_len == length:
                            count += 1
        return count

    def _count_open_sequences(self, board: Board, symbol: str, length: int) -> int:
        """
        Đếm số lượng chuỗi quân liên tiếp có độ dài 'length' của 'symbol'
        mà mở cả hai đầu (tức là có ô trống ở cả hai phía của chuỗi).
        """
        count = 0
        rows, cols = board.rows, board.cols
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for r in range(rows):
            for c in range(cols):
                if board._grid[r][c] == symbol:
                    for dr, dc in directions:
                        prev_r, prev_c = r - dr, c - dc
                        if 0 <= prev_r < rows and 0 <= prev_c < cols and board._grid[prev_r][prev_c] == symbol:
                            continue

                        is_open_start = False
                        if 0 <= prev_r < rows and 0 <= prev_c < cols and board._grid[prev_r][prev_c] == board.EMPTY:
                            is_open_start = True
                        elif not (0 <= prev_r < rows and 0 <= prev_c < cols):
                            pass
                        elif board._grid[prev_r][prev_c] == board.OBSTACLE:
                            pass

                        current_len = 0
                        for k in range(length):
                            cur_r, cur_c = r + k * dr, c + k * dc
                            if 0 <= cur_r < rows and 0 <= cur_c < cols and board._grid[cur_r][cur_c] == symbol:
                                current_len += 1
                            else:
                                break
                        
                        if current_len == length:
                            next_r, next_c = r + length * dr, c + length * dc
                            is_open_end = False
                            if 0 <= next_r < rows and 0 <= next_c < cols and board._grid[next_r][next_c] == board.EMPTY:
                                is_open_end = True
                            elif not (0 <= next_r < rows and 0 <= next_c < cols):
                                pass
                            elif board._grid[next_r][next_c] == board.OBSTACLE:
                                pass
                                
                            if is_open_start and is_open_end:
                                count += 1
        return count

    def _calculate_zobrist_hash(self, board: Board) -> str:
        """
        Tính toán Zobrist Hash cho trạng thái bàn cờ hiện tại.
        """
        current_hash = 0
        for r in range(board.rows):
            for c in range(board.cols):
                symbol = board._grid[r][c]
                current_hash ^= self.zobrist_keys.get((r, c, symbol), 0) 
        return str(current_hash)

    def _get_state_representation(self, board: Board) -> Tuple[str, ...]:
        """
        Tạo một biểu diễn trạng thái bàn cờ dưới dạng tuple để sử dụng cho Q-table.
        """
        return tuple(cell for row in board._grid for cell in row)

    def update_q_table(
        self,
        old_board: Board,
        new_board: Board,
        ai_symbol: str,
        human_symbol: str,
        reward: float,
    ) -> None:
        """
        Cập nhật Q-table cho Q-learning (chỉ dùng cho difficulty "easy").
        """
        if self.last_state is None or self.last_action is None:
            return
        old_state = self.last_state
        r, c = self.last_action
        idx = r * new_board.cols + c
        new_state = self._get_state_representation(new_board)
        cur_q = self.q_table[old_state][idx]
        
        if not self.q_table[new_state]:
            max_next_q = 0.0
        else:
            max_next_q = max(self.q_table[new_state])
            
        self.q_table[old_state][idx] = cur_q + self.learning_rate * (
            reward + self.discount_factor * max_next_q - cur_q
        )
        self.last_state = None
        self.last_action = None

    def get_reward(
        self,
        board: Board,
        ai_symbol: str,
        human_symbol: str,
    ) -> float:
        """
        Tính toán phần thưởng cho Q-learning.
        """
        if board.has_winner_any():
            winner_sym = board.get_winner_symbol()
            if winner_sym == ai_symbol:
                return 1.0  # AI thắng
            elif winner_sym == human_symbol:
                return -1.0  # Người chơi thắng
            else:
                return 0.0
        elif board.is_draw():
            return 0.5
        return 0.0