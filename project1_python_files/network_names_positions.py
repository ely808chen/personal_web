

WARD_NEIGHBORS = {
    '千代田': ['中央区', 'みなと', '新宿区', '文京', '台東'],
    '中央区': ['千代田', 'みなと', '江東区', '台東', '墨田区'],
    'みなと': ['千代田', '中央区', '品川区', '渋谷区', '新宿区'],
    '新宿区': ['千代田', 'みなと', '渋谷区', '中野区', '文京'],
    '文京': ['千代田', '新宿区', '台東', '荒川区', '池袋'],
    '台東': ['千代田', '中央区', '文京', '荒川区', '墨田区'],
    '墨田区': ['中央区', '台東', '江東区', '荒川区', '足立', '葛飾区', '江戸川'],
    '江東区': ['中央区', '墨田区', '江戸川', '品川区'],
    '品川区': ['みなと', '江東区', '大田区', '目黒区', '渋谷区'],
    '目黒区': ['品川区', '大田区', '世田谷', '渋谷区'],
    '大田区': ['品川区', '目黒区', '世田谷'],
    '世田谷': ['大田区', '目黒区', '渋谷区', '杉並'],
    '渋谷区': ['みなと', '新宿区', '目黒区', '世田谷', '杉並', '中野区', '品川区'],
    '中野区': ['新宿区', '渋谷区', '杉並', '池袋', '練馬区'],
    '杉並': ['世田谷', '渋谷区', '中野区', '練馬区'],
    '池袋': ['中野区', '北区', '板橋区', '練馬区'],
    '北区': ['池袋', '板橋区', '荒川区', '足立'],
    '荒川区': ['北区', '台東', '墨田区', '足立'],
    '板橋区': ['北区', '池袋', '練馬区'],
    '練馬区': ['板橋区', '杉並', '中野区', '池袋'],
    '足立': ['荒川区', '墨田区', '葛飾区', '北区'],
    '葛飾区': ['足立', '墨田区', '江戸川', '江戸川'],
    '江戸川': ['葛飾区', '江東区', '葛飾区']
}
# Approximate geographical positions of wards (longitude, latitude)
# These coordinates are approximate center points of each ward
WARD_POSITIONS = {
    '千代田': (139.754, 35.694),
    '中央区': (139.774, 35.671),
    'みなと': (139.751, 35.658),
    '新宿区': (139.710, 35.694),
    '文京': (139.752, 35.708),
    '台東': (139.780, 35.712),
    '墨田区': (139.799, 35.710),
    '江東区': (139.817, 35.673),
    '品川区': (139.730, 35.609),
    '目黒区': (139.698, 35.641),
    '大田区': (139.716, 35.562),
    '世田谷': (139.653, 35.646),
    '渋谷区': (139.703, 35.664),
    '中野区': (139.664, 35.707),
    '杉並': (139.636, 35.699),
    '池袋': (139.717, 35.729),
    '北区': (139.734, 35.752),
    '荒川区': (139.784, 35.736),
    '板橋区': (139.709, 35.751),
    '練馬区': (139.652, 35.735),
    '足立': (139.804, 35.775),
    '葛飾区': (139.847, 35.743),
    '江戸川': (139.868, 35.706)
}