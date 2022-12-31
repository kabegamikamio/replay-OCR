import Levenshtein

# テキストがマップを表しているか
# レーベンシュタイン距離をもとに判定
# マップである場合はマップ名を返す
def ifMap(txt):
    DIST_THRE = 0.5
    map_list = ['ヒメルズドルフ', 'アルペンシュタット', '黒き黄金の村',
                'ミデルブルフ', '運河', 'カスティーリャ', '砂漠の砂',
                '王朝の真珠', 'ファウスト', 'ディスペア砦', '廃工場',
                'ヘラス', 'マヤ遺跡', 'モレンダイク', '沿岸要塞',
                'ニューベイ', 'ノルマンディー', 'オアシスの椰子',
                '港湾', 'ロックフィールド', 'ヴィニヤード', '冬のマリノフカ',
                'ユーコン']
    map_dist = []
    txt = txt.strip()
    for map in map_list:
        lev_dist = Levenshtein.distance(map, txt)
        devider = max([len(txt), len(map)])
        lev_dist = lev_dist / devider
        lev_dist = 1 - lev_dist
        map_dist.append(lev_dist)
    if(max(map_dist) >= DIST_THRE):
        return map_list[map_dist.index(max(map_dist))]
    else:
        return False

# テキストが優勢戦のロード画面を表しているか
# レーベンシュタイン距離をもとに判定
# ロード画面である場合はTrueを返す
def ifLoading(txt):
    DIST_THRE = 0.5
    desc = '陣地を占領し、敵車輌を撃破せよ。'
    txt = txt.strip()
    lev_dist = Levenshtein.distance(desc, txt)
    devider = max([len(txt), len(desc)])
    lev_dist = lev_dist / devider
    lev_dist = 1 - lev_dist
    if(lev_dist > DIST_THRE):
        return True
    else:
        return False

# テキストが勝敗を表しているか
# 勝敗を表す場合勝敗とその理由を返す
# 0: 勝敗データなし
# 1: 勝利(殲滅), 2: 敗北(殲滅), 3: 勝利(ポイント), 4: 敗北(ポイント)
def ifResult(txt):
    DIST_THRE = 0.5
    result_dist = []
    result_list = ['勝利!敵車輌が全滅した', '敗北!味方車輌が全滅した',
                    '勝利!味方チームが1,000勝利ポイントを獲得',
                    '敗北!敵チームが1,000勝利ポイントを獲得']
    txt = txt.strip()
    for i in result_list:
        lev_dist = Levenshtein.distance(i, txt)
        devider = max([len(txt), len(i)])
        lev_dist = lev_dist / devider
        lev_dist = 1 - lev_dist
        result_dist.append(lev_dist)
    if(max(result_dist) >= DIST_THRE):
        reason = result_dist.index(max(result_dist))
        return reason+1
    else:
        return False