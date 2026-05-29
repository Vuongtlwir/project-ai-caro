Thống Nhất Khi Làm  

1. Structure project 

src/ 

ai/ 

game/ 

ui/ 

utils/ 

docs/ 

2. Format board 

board[row][col] 

3. Format move 

(row, col) 

4. API board 

make_move() 

undo_move() 

is_valid_move() 

get_valid_moves() 

check_win() 

switch_player() 

5. API AI 

get_best_move(board, player) 

evaluate_board(board, player) 

minimax(...) 

6. Luật game 

thắng 5 quân 

có overline không 

có double-three không 

8. Search settings 

MAX_DEPTH 

TIME_LIMIT 

9. Move generation 

xét nearby moves 

thứ tự move ordering 

10. Undo move 

restore đúng board 

restore turn 

restore cache/state nếu có 

11. Coding style 

format name get_bet_move()  k dùng GetBestMove() 

comment lại các phần quan trọng 