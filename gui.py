import pygame, random
_STARS = [(random.randint(0, 1200), random.randint(0, 2500), 1) for _ in range(140)]
_bg_cache = None
_bg_size = (0,0)

def draw_bg(surf):
    global _bg_cache, _bg_size
    W,H=surf.get_size()
    if _bg_cache is None or _bg_size!=(W,H):
        _bg_size=(W,H)
        _bg_cache=pygame.Surface((W,H))
        for y in range(H):
            t=y/H
            r=int(6+t*14); g=int(12+t*20); b=int(30+t*38)
            pygame.draw.line(_bg_cache,(r,g,b),(0,y),(W,y))
        for sx,sy,_ in _STARS:
            if 0<sx<W and 0<sy<H:
                pygame.draw.circle(_bg_cache,(90,120,200),(sx,sy),1)
    surf.blit(_bg_cache,(0,0))

def draw_side_borders(surf):
    W,H=surf.get_size()
    bw=20
    pygame.draw.rect(surf,(5,10,25),(0,0,bw+6,H))
    pygame.draw.rect(surf,(5,10,25),(W-bw-6,0,bw+6,H))
    pygame.draw.rect(surf,(0,235,255),(0,0,bw,H))
    pygame.draw.rect(surf,(0,235,255),(W-bw,0,bw,H))

def draw_glass(surf,rect,rad=20,alpha=115,border=True):
    s=pygame.Surface((rect.w,rect.h),pygame.SRCALPHA)
    pygame.draw.rect(s,(20,35,75,alpha),(0,0,rect.w,rect.h),border_radius=rad)
    surf.blit(s,rect.topleft)
    if border:
        pygame.draw.rect(surf,(0,220,255),rect,width=1,border_radius=rad)

def _joint(surf,cx,cy,size,col,glow=False):
    r=int(size*0.15)
    pygame.draw.circle(surf,(10,15,30),(cx,cy),r+3)
    pygame.draw.circle(surf,(35,45,75),(cx,cy),r+1)
    pygame.draw.circle(surf,col,(cx,cy),int(r*0.7))
    if glow:
        pygame.draw.circle(surf,col,(cx,cy),r+7,2)

def draw_pipe(surf,pipes_dict,p_type,x,y,size,is_start=False,is_end=False,is_empty=False,is_block=False,flow_level=0,tick=0,water_percent=0,is_tray=False,valid_hint=False):
    cx,cy=x+size//2,y+size//2
    if is_block: return
    if is_start:
        pygame.draw.rect(surf,(0,50,80),(x+2,y+2,size-4,size-4),border_radius=12)
        pygame.draw.rect(surf,(0,235,255),(x+4,y+4,size-8,size-8),border_radius=10)
        if water_percent>0.01:
            h=int((size-12)*water_percent)
            pygame.draw.rect(surf,(0,180,255),(x+6,y+size-6-h,size-12,h),border_radius=7)
        return
    if is_end:
        pygame.draw.rect(surf,(90,100,115),(x+2,y+2,size-4,size-4),border_radius=12)
        pygame.draw.rect(surf,(240,245,255),(x+4,y+4,size-8,size-8),border_radius=10)
        if water_percent>0.01:
            h=int((size-12)*water_percent)
            pygame.draw.rect(surf,(0,255,130),(x+6,y+size-6-h,size-12,h),border_radius=7)
        return
    if is_empty:
        pygame.draw.circle(surf,(12,20,42),(cx,cy),int(size*0.26))
        pygame.draw.circle(surf,(60,75,105),(cx,cy),int(size*0.10))
        return
    if p_type not in pipes_dict: return
    col_main=(0,255,140) if (is_tray or valid_hint) else (210,225,245)
    if flow_level>0: col_main=(0,230,255)
    length=size//2
    for d in pipes_dict[p_type]:
        ex,ey=cx,cy
        if d==0: ey=cy-length
        if d==1: ex=cx+length
        if d==2: ey=cy+length
        if d==3: ex=cx-length
        th=int(size*0.20)
        pygame.draw.line(surf,(0,5,20),(cx,cy),(ex,ey),th+4)
        pygame.draw.line(surf,col_main,(cx,cy),(ex,ey),th)
    _joint(surf,cx,cy,size,col_main,glow=is_tray or flow_level>0)

def draw_board(screen,board,solution,gs,logic,tick):
    if gs.flow_active:
        p=gs.anim/max(1,len(gs.win_path))
        p=max(0,min(1,p))
        gs.start_tank=1.0-p
        gs.end_tank=p
    else:
        if not hasattr(gs,'start_tank'): gs.start_tank=1.0
        if not hasattr(gs,'end_tank'): gs.end_tank=0.0
    for r in range(len(board)):
        for c in range(len(board[0])):
            x=gs.GX+c*gs.CELL; y=gs.GY+r*gs.CELL
            val=board[r][c]
            if val=='BLOCK': continue
            fl=0
            if gs.flow_active and (r,c) in gs.win_path:
                try:
                    if gs.win_path.index((r,c))<=int(gs.anim): fl=2
                except: pass
            wp=getattr(gs,'start_tank',1.0) if val=='START' else getattr(gs,'end_tank',0.0) if val=='END' else 0
            if val is None:
                draw_pipe(screen,logic.PIPES,solution.get((r,c),'I_h'),x,y,gs.CELL,is_empty=True)
            elif val=='START':
                draw_pipe(screen,logic.PIPES,'I_h',x,y,gs.CELL,is_start=True,water_percent=wp)
            elif val=='END':
                draw_pipe(screen,logic.PIPES,'I_h',x,y,gs.CELL,is_end=True,water_percent=wp)
            else:
                draw_pipe(screen,logic.PIPES,val,x,y,gs.CELL,flow_level=fl,valid_hint=solution.get((r,c))==val)