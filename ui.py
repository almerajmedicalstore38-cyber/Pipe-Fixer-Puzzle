import pygame, gui
from game_state import GRID
def draw_all(screen, gs, logic, wallet, config, wrong_highlight, selected_cell, hover_valid, box_x, box_y, box_size, hint_btn, flow_btn, undo_btn, lvl_btn, wallet_btn, coins_btn, mute_btn, is_muted):
    gui.draw_bg(screen); gui.draw_side_borders(screen)
    top_rect=pygame.Rect(config.INNER_X,int(config.H*0.015),config.INNER_W,int(config.H*0.065)); gui.draw_glass(screen,top_rect,20)
    for rect in (lvl_btn,wallet_btn,coins_btn,mute_btn): pygame.draw.rect(screen,(28,45,95),rect,border_radius=12)
    pygame.draw.rect(screen,(15,25,55),lvl_btn,border_radius=12)
    screen.blit(config.F_TOP.render(f"L{gs.level}",True,(0,230,255)),config.F_TOP.render(f"L{gs.level}",True,(0,230,255)).get_rect(center=lvl_btn.center))
    screen.blit(config.F_SMALL.render("WALLET",True,(255,215,0)),config.F_SMALL.render("WALLET",True,(255,215,0)).get_rect(center=wallet_btn.center))
    screen.blit(config.F_SMALL.render(f"C:{wallet.data['coins']}",True,(255,215,0)),config.F_SMALL.render(f"C:{wallet.data['coins']}",True,(255,215,0)).get_rect(center=coins_btn.center))
    screen.blit(config.F_TOP.render("OFF" if is_muted else "ON",True,(255,80,80) if is_muted else (0,255,130)),config.F_TOP.render("OFF" if is_muted else "ON",True,(255,80,80) if is_muted else (0,255,130)).get_rect(center=mute_btn.center))
    board_bg_rect=pygame.Rect(config.INNER_X,gs.GY-6,config.INNER_W,GRID*gs.CELL+12); gui.draw_glass(screen,board_bg_rect,22)
    tray_rect=pygame.Rect(config.INNER_X,gs.GY+GRID*gs.CELL+18,config.INNER_W,gs.CELL+16+36); gui.draw_glass(screen,tray_rect,22)
    pygame.draw.rect(screen,(0,230,255),hint_btn,border_radius=14)
    screen.blit(config.F_HINT.render(f"HINT - {config.HINT_COST}C + AD",True,(255,255,255)),(hint_btn.centerx-70,hint_btn.centery-9))
    pygame.draw.rect(screen,(15,22,45),(box_x,box_y,box_size,box_size),border_radius=14)
    pygame.draw.rect(screen,(0,255,130) if hover_valid else (0,230,255),(box_x,box_y,box_size,box_size),width=2,border_radius=14)
    pygame.draw.rect(screen,(0,230,255),flow_btn,border_radius=22)
    pygame.draw.rect(screen,(255,135,0),undo_btn,border_radius=16)
    screen.blit(config.F_FLOW.render("FLOW",True,(0,0,0)),(flow_btn.centerx-26,flow_btn.centery-9))
    screen.blit(config.F_HINT.render("REMOVE" if selected_cell else "UNDO",True,(0,0,0)),(undo_btn.centerx-28,undo_btn.centery-9))
    gui.draw_board(screen,gs.board,gs.solution,gs,logic,0)
    if wrong_highlight:
        for r,c in wrong_highlight: pygame.draw.rect(screen,(255,40,40),(gs.GX+c*gs.CELL-3,gs.GY+r*gs.CELL-3,gs.CELL+6,gs.CELL+6),width=4,border_radius=10)
    if selected_cell:
        r,c=selected_cell
        pygame.draw.rect(screen,(255,255,0),(gs.GX+c*gs.CELL-3,gs.GY+r*gs.CELL-3,gs.CELL+6,gs.CELL+6),width=4,border_radius=10)
    if gs.current_pipe and not gs.drag: gui.draw_pipe(screen,logic.PIPES,gs.current_pipe,box_x+6,box_y+6,gs.CELL-2,is_tray=True)