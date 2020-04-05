from modules.Agent import Agent
from modules.Game import Game
import numpy as np



class PlayABunchOfGames():
    
    def __init__(self, players, loop=100):
        self.players = players
        self.loop = loop
        self.all_games_moves = [] # each element is [ q_moves, [ [board1, move1], [board2, move2] ] ]
    

    def start(self):
        for iteration in range(self.loop):
            print('\tplaying game {}/{}'.format(iteration, self.loop))
            # Make a game
            self.game = Game(
                players=self.players,
                print_board_state=False
            )
            self.game.start()
            if self.game.winner:
                winner_moves = self.game.get_winner_moves()
                self.all_games_moves.append([
                    self.game.move_number,
                    [[move['board_state'], move['move']] for move in winner_moves]
                ])
    

    def get_moves_faster_than_average(self, top_percentage):
        """
        Returns the moves of the games that were won in less than the average number of moves
        Arguments:
        - top_percentage (float): games that finished in less than average_moves * top_percentage moves will be returned.
        """
        q_moves_list = [iteration[0] for iteration in self.all_games_moves]
        if len(q_moves_list) == 0:
            print('This is wrong. This should not happen. But guess what? It happened!')
            return []
        q_moves_average = sum(q_moves_list) / len(q_moves_list)
        threshold = np.ceil(q_moves_average * top_percentage)
        top_moves = []
        for game_moves in self.all_games_moves:
            if game_moves[0] < threshold:
                top_moves += game_moves[1]
        print('Average number of moves:', q_moves_average)
        print('\tThreshold: {}\tQ top moves: {}', threshold, len(top_moves))
        return top_moves


    def get_top_moves(self, top_percentage=0.5):
        """
        Returns the top X% moves ordered by number of moves
        Arguments:
        - top_percentage (float): pecentage of moves to return. Defaults to 50%
        """
        # Sort moves based on q_moves
        self.all_games_moves.sort(key = lambda move: move[0]) # the first element on the list is the number of moves of that game
        q_games = len(self.all_games_moves)
        top_moves = []
        for move in self.all_games_moves[0:int(q_games * top_percentage)]:
            top_moves += move[1]

        # Find the distribution of moves (ie if all the moves are number 3, that's not very helpful)
        distribution = {}
        for top_move in top_moves:
            distribution[top_move[1]] = distribution.get(top_move[1], 0) + 1
        # Find the move that was less chosen
        less_chosen_move_q = np.inf
        for key in distribution.keys():
            if distribution[key] < less_chosen_move_q:
                less_chosen_move_q = distribution[key]
                less_chosen_move = key
        # Limit the selection of moves to have them all be the same number
        moves_selected = {}
        top_moves_evenly_distributed = []
        for top_move in top_moves:
            if moves_selected.get(top_move[1], 0) < less_chosen_move_q:
                moves_selected[top_move[1]] = moves_selected.get(top_move[1], 0) + 1
                top_moves_evenly_distributed.append(top_move)

        # print('top move element')
        # print(top_moves[0])
        # print(distribution)
        # print(less_chosen_move_q)
        # print(less_chosen_move)
        # print(moves_selected)
        # print(len(top_moves_evenly_distributed))
        # print(top_moves_evenly_distributed[0])
        return top_moves_evenly_distributed