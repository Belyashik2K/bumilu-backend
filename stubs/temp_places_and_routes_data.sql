WITH lang_list AS (SELECT *
                   FROM (VALUES ('RU'::language_enum),
                                ('EN'::language_enum),
                                ('ZH'::language_enum)) AS t(language_code)),

     phone_type_list AS (SELECT pt.phone_type,
                                row_number() OVER (ORDER BY pt.phone_type::text) AS rn
                         FROM (SELECT unnest(enum_range(NULL::place_phone_type_enum)) AS phone_type) pt),

     primary_phone_type AS (SELECT ptl.phone_type
                            FROM phone_type_list ptl
                            WHERE ptl.rn = 1),

     secondary_phone_type AS (SELECT COALESCE(
                                             (SELECT ptl.phone_type FROM phone_type_list ptl WHERE ptl.rn = 2),
                                             (SELECT ptl.phone_type FROM phone_type_list ptl WHERE ptl.rn = 1)
                                     ) AS phone_type),

     category_seed AS (SELECT *
                       FROM (VALUES ('cafe', 'coffee', '#C67C4E', 'Кафе', 'Cafe', '咖啡馆'),
                                    ('museum', 'landmark', '#3B82F6', 'Музей', 'Museum', '博物馆'),
                                    ('park', 'trees', '#22C55E', 'Парк', 'Park', '公园'),
                                    ('landmark', 'star', '#F59E0B', 'Достопримечательность', 'Landmark', '地标'),
                                    ('viewpoint', 'binoculars', '#8B5CF6', 'Смотровая площадка', 'Viewpoint',
                                     '观景点')) AS t(slug, icon_key, marker_color, name_ru, name_en, name_zh)),

     ins_categories AS (
         INSERT INTO place_categories (
                                       id,
                                       slug,
                                       icon_key,
                                       marker_color,
                                       created_at,
                                       updated_at
             )
             SELECT uuidv7(),
                    cs.slug,
                    cs.icon_key,
                    cs.marker_color,
                    now(),
                    now()
             FROM category_seed cs
             RETURNING
                 place_categories.id AS category_id,
                 place_categories.slug AS category_slug),

     ins_category_translations AS (
         INSERT
             INTO place_category_translations (id,
                                               category_id,
                                               language_code,
                                               name,
                                               created_at,
                                               updated_at)
                 SELECT uuidv7(),
                        ic.category_id,
                        ll.language_code,
                        CASE ll.language_code
                            WHEN 'RU'::language_enum THEN cs.name_ru
                            WHEN 'EN'::language_enum THEN cs.name_en
                            WHEN 'ZH'::language_enum THEN cs.name_zh
                            END,
                        now(),
                        now()
                 FROM ins_categories ic
                          JOIN category_seed cs
                               ON cs.slug = ic.category_slug
                          CROSS JOIN lang_list ll
                 RETURNING 1),

     place_seed AS (SELECT *
                    FROM (VALUES ('hermitage', 'museum', 30.314566:: double precision, 59.939864:: double precision,
                                  'Эрмитаж', 'Hermitage Museum', '埃尔米塔日博物馆',
                                  'Главный музей России на Дворцовой площади.',
                                  'The main museum of Russia on Palace Square.', '位于宫殿广场的俄罗斯主要博物馆。',
                                  'Один из крупнейших музеев мира.', 'One of the largest museums in the world.',
                                  '世界上最大的博物馆之一。', 'Дворцовая площадь, 2', 'Palace Square, 2', '宫殿广场2号',
                                  'Дворцовая площадь, 2', 'Вход со стороны площади'),
                                 ('isaac', 'landmark', 30.306125:: double precision, 59.934081:: double precision,
                                  'Исаакиевский собор', 'Saint Isaac’s Cathedral', '圣以撒大教堂',
                                  'Один из символов Санкт-Петербурга с колоннадой.',
                                  'One of Saint Petersburg’s symbols with a famous colonnade.',
                                  '圣彼得堡的象征之一，以柱廊闻名。', 'Знаменитый собор с панорамным видом.',
                                  'Famous cathedral with panoramic views.', '著名教堂，可俯瞰全景。',
                                  'Исаакиевская площадь, 4', 'St. Isaac’s Square, 4', '圣以撒广场4号',
                                  'Исаакиевская площадь, 4', 'Удобнее подъезжать с Исаакиевской площади'),
                                 ('kazan', 'landmark', 30.324538:: double precision, 59.934208:: double precision,
                                  'Казанский собор', 'Kazan Cathedral', '喀山大教堂',
                                  'Знаменитый собор на Невском проспекте.', 'Famous cathedral on Nevsky Prospekt.',
                                  '位于涅瓦大街上的著名大教堂。', 'Главный храм центра города.',
                                  'A major cathedral in the city center.', '市中心的重要教堂。', 'Казанская площадь, 2',
                                  'Kazan Square, 2', '喀山广场2号', 'Казанская площадь, 2',
                                  'Высадка у Невского проспекта'),
                                 ('savior', 'landmark', 30.328633:: double precision, 59.940070:: double precision,
                                  'Спас на Крови', 'Church of the Savior on Spilled Blood', '滴血救世主教堂',
                                  'Яркий храм с мозаиками у канала Грибоедова.',
                                  'Colorful church with mosaics by Griboyedov Canal.',
                                  '格里博耶多夫运河旁色彩鲜艳、饰有马赛克的教堂。',
                                  'Один из самых узнаваемых храмов города.',
                                  'One of the most recognizable churches in the city.', '城市中最具辨识度的教堂之一。',
                                  'наб. канала Грибоедова, 2Б', 'Griboyedov Canal Embankment, 2B',
                                  '格里博耶多夫运河堤岸2B', 'наб. канала Грибоедова, 2Б',
                                  'Подъезд удобнее со стороны канала'),
                                 ('summer_garden', 'park', 30.335553:: double precision, 59.944908:: double precision,
                                  'Летний сад', 'Summer Garden', '夏园', 'Исторический парк с аллеями и скульптурами.',
                                  'Historic garden with alleys and sculptures.', '拥有林荫道和雕塑的历史花园。',
                                  'Тихое место для прогулки в центре.', 'A peaceful walking spot in the center.',
                                  '市中心安静的散步地点。', 'Летний сад', 'Summer Garden', '夏园', 'Летний сад',
                                  'Подъезд к входу со стороны набережной'),
                                 ('new_holland', 'park', 30.289633:: double precision, 59.929643:: double precision,
                                  'Новая Голландия', 'New Holland Island', '新荷兰岛',
                                  'Современное общественное пространство на острове.',
                                  'Modern public space on a renovated island.', '翻新的岛上现代公共空间。',
                                  'Популярное место для отдыха и еды.', 'Popular place for leisure and food.',
                                  '热门休闲和餐饮地点。', 'наб. Адмиралтейского канала, 2',
                                  'Admiralty Canal Embankment, 2', '海军运河堤岸2号', 'наб. Адмиралтейского канала, 2',
                                  'Такси лучше вызывать ко входу с набережной'),
                                 ('sevkabel', 'viewpoint', 30.240923:: double precision, 59.924126:: double precision,
                                  'Севкабель Порт', 'Sevkabel Port', '塞夫卡贝尔港',
                                  'Пространство у Финского залива с прогулочной линией.',
                                  'Waterfront cultural space by the Gulf of Finland.', '芬兰湾畔的滨水文化空间。',
                                  'Хорошее место для заката.', 'Great place for sunset.', '看日落的好地方。',
                                  'Кожевенная линия, 40', 'Kozhevennaya Line, 40', '科热文纳亚线40号',
                                  'Кожевенная линия, 40', 'Подъезд со стороны главного входа'),
                                 ('dvorcovy_bridge', 'viewpoint', 30.308017:: double precision,
                                  59.941238:: double precision, 'Дворцовый мост', 'Palace Bridge', '宫殿桥',
                                  'Знаменитый разводной мост в центре Петербурга.',
                                  'Famous drawbridge in the center of Saint Petersburg.', '圣彼得堡市中心著名的开合桥。',
                                  'Популярная точка для фото и прогулок.', 'Popular spot for photos and walks.',
                                  '热门拍照和散步地点。', 'Дворцовый мост', 'Palace Bridge', '宫殿桥', 'Дворцовый мост',
                                  'Лучше высадка у Адмиралтейской набережной'),
                                 ('bolshe_coffee', 'cafe', 30.320560:: double precision, 59.954486:: double precision,
                                  'Больше кофе!', 'Bolshe Coffee!', '更多咖啡',
                                  'Популярная кофейня рядом с Марсовым полем.',
                                  'Popular coffee spot near Marsovo Pole.', '马尔索沃广场附近的热门咖啡馆。',
                                  'Кофе и десерты в центре города.', 'Coffee and desserts in the city center.',
                                  '市中心的咖啡和甜点。', 'наб. реки Мойки, 7', 'Moika River Embankment, 7',
                                  '莫伊卡河堤岸7号', 'наб. реки Мойки, 7', 'Подъезд со стороны Мойки'),
                                 ('skuratov', 'cafe', 30.320425:: double precision, 59.958019:: double precision,
                                  'Skuratov Coffee', 'Skuratov Coffee', '斯库拉托夫咖啡',
                                  'Современная кофейня в центре Петербурга.',
                                  'Modern coffee shop in central Saint Petersburg.', '圣彼得堡市中心的现代咖啡馆。',
                                  'Спешелти кофе и спокойная атмосфера.', 'Specialty coffee and a calm atmosphere.',
                                  '精品咖啡和安静氛围。', 'Гороховая улица, 41', 'Gorokhovaya Street, 41',
                                  '戈罗霍瓦亚街41号', 'Гороховая улица, 41',
                                  'Удобно подъезжать с Гороховой улицы')) AS t(
                                                                               place_code, category_slug, lon, lat,
                                                                               title_ru, title_en, title_zh,
                                                                               description_ru, description_en,
                                                                               description_zh, short_description_ru,
                                                                               short_description_en,
                                                                               short_description_zh, address_display_ru,
                                                                               address_display_en, address_display_zh,
                                                                               address_taxi, address_taxi_comment
                        )),
     prepared_places AS (SELECT uuidv7()       AS place_id,
                                ic.category_id AS category_id,
                                ps.place_code,
                                ps.lon,
                                ps.lat,
                                ps.title_ru,
                                ps.title_en,
                                ps.title_zh,
                                ps.description_ru,
                                ps.description_en,
                                ps.description_zh,
                                ps.short_description_ru,
                                ps.short_description_en,
                                ps.short_description_zh,
                                ps.address_display_ru,
                                ps.address_display_en,
                                ps.address_display_zh,
                                ps.address_taxi,
                                ps.address_taxi_comment
                         FROM place_seed ps
                                  JOIN ins_categories ic
                                       ON ic.category_slug = ps.category_slug),

     ins_places AS (
         INSERT
             INTO places (id,
                          category_id,
                          location,
                          timezone,
                          address_taxi,
                          address_taxi_comment,
                          created_at,
                          updated_at)
                 SELECT pp.place_id,
                        pp.category_id,
                        ST_SetSRID(ST_MakePoint(pp.lon, pp.lat), 4326)::geography,
                        'Europe/Moscow',
                        pp.address_taxi,
                        pp.address_taxi_comment,
                        now(),
                        now()
                 FROM prepared_places pp
                 RETURNING
                     places.id AS place_id),
     place_map AS (SELECT pp.place_id,
                          pp.place_code,
                          pp.title_ru,
                          pp.title_en,
                          pp.title_zh,
                          pp.description_ru,
                          pp.description_en,
                          pp.description_zh,
                          pp.short_description_ru,
                          pp.short_description_en,
                          pp.short_description_zh,
                          pp.address_display_ru,
                          pp.address_display_en,
                          pp.address_display_zh
                   FROM prepared_places pp),
     ins_place_translations AS (
         INSERT
             INTO place_translations (id,
                                      place_id,
                                      language_code,
                                      title,
                                      description,
                                      short_description,
                                      address_display,
                                      created_at,
                                      updated_at)
                 SELECT uuidv7(),
                        pm.place_id,
                        ll.language_code,
                        CASE ll.language_code
                            WHEN 'RU'::language_enum THEN pm.title_ru
                            WHEN 'EN'::language_enum THEN pm.title_en
                            WHEN 'ZH'::language_enum THEN pm.title_zh
                            END,
                        CASE ll.language_code
                            WHEN 'RU'::language_enum THEN pm.description_ru
                            WHEN 'EN'::language_enum THEN pm.description_en
                            WHEN 'ZH'::language_enum THEN pm.description_zh
                            END,
                        CASE ll.language_code
                            WHEN 'RU'::language_enum THEN pm.short_description_ru
                            WHEN 'EN'::language_enum THEN pm.short_description_en
                            WHEN 'ZH'::language_enum THEN pm.short_description_zh
                            END,
                        CASE ll.language_code
                            WHEN 'RU'::language_enum THEN pm.address_display_ru
                            WHEN 'EN'::language_enum THEN pm.address_display_en
                            WHEN 'ZH'::language_enum THEN pm.address_display_zh
                            END,
                        now(),
                        now()
                 FROM place_map pm
                          CROSS JOIN lang_list ll
                 RETURNING 1),
     place_numbered AS (SELECT pm.place_id,
                               pm.place_code,
                               row_number() OVER (ORDER BY pm.place_code) AS rn
                        FROM place_map pm),
     ins_place_primary_phones AS (
         INSERT
             INTO place_phones (id,
                                place_id,
                                number,
                                type,
                                is_primary,
                                created_at,
                                updated_at)
                 SELECT uuidv7(),
                        pn.place_id,
                        '+7812' || lpad((1000000 + pn.rn)::text, 7, '0'),
                        ppt.phone_type,
                        true,
                        now(),
                        now()
                 FROM place_numbered pn
                          CROSS JOIN primary_phone_type ppt
                 RETURNING 1),
     ins_place_secondary_phones AS (
         INSERT
             INTO place_phones (id,
                                place_id,
                                number,
                                type,
                                is_primary,
                                created_at,
                                updated_at)
                 SELECT uuidv7(),
                        pn.place_id,
                        '+7965' || lpad((2000000 + pn.rn)::text, 7, '0'),
                        spt.phone_type,
                        false,
                        now(),
                        now()
                 FROM place_numbered pn
                          CROSS JOIN secondary_phone_type spt
                 WHERE (pn.rn % 2) = 1
                 RETURNING 1)
        ,
     working_hours_seed AS (SELECT *
                            FROM (VALUES ('hermitage', 1, time '11:00', time '20:00'),
                                         ('hermitage', 2, time '11:00', time '20:00'),
                                         ('hermitage', 3, time '11:00', time '20:00'),
                                         ('hermitage', 4, time '11:00', time '20:00'),
                                         ('hermitage', 5, time '11:00', time '20:00'),
                                         ('hermitage', 6, time '11:00', time '20:00'),
                                         ('hermitage', 7, time '11:00', time '18:00'),
                                         ('isaac', 1, time '10:00', time '21:30'),
                                         ('isaac', 2, time '10:00', time '21:30'),
                                         ('isaac', 3, time '10:00', time '21:30'),
                                         ('isaac', 4, time '10:00', time '21:30'),
                                         ('isaac', 5, time '10:00', time '21:30'),
                                         ('isaac', 6, time '10:00', time '21:30'),
                                         ('isaac', 7, time '10:00', time '21:30'),
                                         ('kazan', 1, time '09:00', time '20:00'),
                                         ('kazan', 2, time '09:00', time '20:00'),
                                         ('kazan', 3, time '09:00', time '20:00'),
                                         ('kazan', 4, time '09:00', time '20:00'),
                                         ('kazan', 5, time '09:00', time '20:00'),
                                         ('kazan', 6, time '09:00', time '20:00'),
                                         ('kazan', 7, time '09:00', time '20:00'),
                                         ('savior', 1, time '10:30', time '18:00'),
                                         ('savior', 2, time '10:30', time '18:00'),
                                         ('savior', 3, time '10:30', time '18:00'),
                                         ('savior', 4, time '10:30', time '18:00'),
                                         ('savior', 5, time '10:30', time '18:00'),
                                         ('savior', 6, time '10:30', time '18:00'),
                                         ('savior', 7, time '10:30', time '18:00'),
                                         ('summer_garden', 1, time '10:00', time '20:00'),
                                         ('summer_garden', 2, time '10:00', time '20:00'),
                                         ('summer_garden', 3, time '10:00', time '20:00'),
                                         ('summer_garden', 4, time '10:00', time '20:00'),
                                         ('summer_garden', 5, time '10:00', time '20:00'),
                                         ('summer_garden', 6, time '10:00', time '20:00'),
                                         ('summer_garden', 7, time '10:00', time '20:00'),
                                         ('new_holland', 1, time '10:00', time '22:00'),
                                         ('new_holland', 2, time '10:00', time '22:00'),
                                         ('new_holland', 3, time '10:00', time '22:00'),
                                         ('new_holland', 4, time '10:00', time '22:00'),
                                         ('new_holland', 5, time '10:00', time '22:00'),
                                         ('new_holland', 6, time '10:00', time '23:00'),
                                         ('new_holland', 7, time '10:00', time '23:00'),
                                         ('sevkabel', 1, time '10:00', time '22:00'),
                                         ('sevkabel', 2, time '10:00', time '22:00'),
                                         ('sevkabel', 3, time '10:00', time '22:00'),
                                         ('sevkabel', 4, time '10:00', time '22:00'),
                                         ('sevkabel', 5, time '10:00', time '22:00'),
                                         ('sevkabel', 6, time '10:00', time '23:00'),
                                         ('sevkabel', 7, time '10:00', time '23:00'),
                                         ('dvorcovy_bridge', 1, time '00:00', time '23:59'),
                                         ('dvorcovy_bridge', 2, time '00:00', time '23:59'),
                                         ('dvorcovy_bridge', 3, time '00:00', time '23:59'),
                                         ('dvorcovy_bridge', 4, time '00:00', time '23:59'),
                                         ('dvorcovy_bridge', 5, time '00:00', time '23:59'),
                                         ('dvorcovy_bridge', 6, time '00:00', time '23:59'),
                                         ('dvorcovy_bridge', 7, time '00:00', time '23:59'),
                                         ('bolshe_coffee', 1, time '08:00', time '22:00'),
                                         ('bolshe_coffee', 2, time '08:00', time '22:00'),
                                         ('bolshe_coffee', 3, time '08:00', time '22:00'),
                                         ('bolshe_coffee', 4, time '08:00', time '22:00'),
                                         ('bolshe_coffee', 5, time '08:00', time '22:00'),
                                         ('bolshe_coffee', 6, time '09:00', time '22:00'),
                                         ('bolshe_coffee', 7, time '09:00', time '22:00'),
                                         ('skuratov', 1, time '08:00', time '22:00'),
                                         ('skuratov', 2, time '08:00', time '22:00'),
                                         ('skuratov', 3, time '08:00', time '22:00'),
                                         ('skuratov', 4, time '08:00', time '22:00'),
                                         ('skuratov', 5, time '08:00', time '22:00'),
                                         ('skuratov', 6, time '09:00', time '22:00'),
                                         ('skuratov', 7, time '09:00',
                                          time '22:00')) AS t(place_code, weekday, start_time, end_time)),
     ins_place_working_hours AS (
         INSERT
             INTO place_working_hours (id,
                                       place_id,
                                       weekday,
                                       start_time,
                                       end_time,
                                       created_at,
                                       updated_at)
                 SELECT uuidv7(),
                        pm.place_id,
                        whs.weekday,
                        whs.start_time,
                        whs.end_time,
                        now(),
                        now()
                 FROM working_hours_seed whs
                          JOIN place_map pm
                               ON pm.place_code = whs.place_code
                 RETURNING 1),

     route_seed AS (SELECT *
                    FROM (VALUES (1, 'classic_center', 'Классический центр Петербурга',
                                  'Classic Center of Saint Petersburg', '圣彼得堡经典市中心',
                                  'Главные символы центра города.', 'Main landmarks of the city center.',
                                  '市中心主要地标。', 'Маршрут по главным достопримечательностям исторического центра.',
                                  'A route through the major landmarks of the historic center.',
                                  '穿越历史中心主要景点的路线。'),
                                 (2, 'modern_spb', 'Современный Петербург', 'Modern Saint Petersburg', '现代圣彼得堡',
                                  'Кофе, прогулки и общественные пространства.',
                                  'Coffee, walks, and modern public spaces.', '咖啡、散步和现代公共空间。',
                                  'Маршрут для прогулки по современным и атмосферным точкам города.',
                                  'A route through atmospheric modern spots in the city.',
                                  '穿越城市现代氛围地点的路线。')) AS t(
                                                                       route_no, route_code, title_ru, title_en,
                                                                       title_zh, short_description_ru,
                                                                       short_description_en, short_description_zh,
                                                                       description_ru, description_en, description_zh
                        )),
     prepared_routes AS (SELECT uuidv7() AS route_id,
                                rs.route_no,
                                rs.route_code,
                                rs.title_ru,
                                rs.title_en,
                                rs.title_zh,
                                rs.short_description_ru,
                                rs.short_description_en,
                                rs.short_description_zh,
                                rs.description_ru,
                                rs.description_en,
                                rs.description_zh
                         FROM route_seed rs),
     ins_routes AS (
         INSERT
             INTO routes (id,
                          created_at,
                          updated_at)
                 SELECT pr.route_id,
                        now(),
                        now()
                 FROM prepared_routes pr
                 RETURNING
                     routes.id AS route_id),
     route_map AS (SELECT pr.route_id,
                          pr.route_no,
                          pr.route_code,
                          pr.title_ru,
                          pr.title_en,
                          pr.title_zh,
                          pr.short_description_ru,
                          pr.short_description_en,
                          pr.short_description_zh,
                          pr.description_ru,
                          pr.description_en,
                          pr.description_zh
                   FROM prepared_routes pr),
     ins_route_translations AS (
         INSERT
             INTO route_translations (id,
                                      route_id,
                                      language_code,
                                      title,
                                      short_description,
                                      description,
                                      created_at,
                                      updated_at)
                 SELECT uuidv7(),
                        rm.route_id,
                        ll.language_code,
                        CASE ll.language_code
                            WHEN 'RU'::language_enum THEN rm.title_ru
                            WHEN 'EN'::language_enum THEN rm.title_en
                            WHEN 'ZH'::language_enum THEN rm.title_zh
                            END,
                        CASE ll.language_code
                            WHEN 'RU'::language_enum THEN rm.short_description_ru
                            WHEN 'EN'::language_enum THEN rm.short_description_en
                            WHEN 'ZH'::language_enum THEN rm.short_description_zh
                            END,
                        CASE ll.language_code
                            WHEN 'RU'::language_enum THEN rm.description_ru
                            WHEN 'EN'::language_enum THEN rm.description_en
                            WHEN 'ZH'::language_enum THEN rm.description_zh
                            END,
                        now(),
                        now()
                 FROM route_map rm
                          CROSS JOIN lang_list ll
                 RETURNING 1),
     route_point_seed AS (SELECT *
                          FROM (VALUES (1, 1, 'hermitage'),
                                       (1, 2, 'isaac'),
                                       (1, 3, 'kazan'),
                                       (1, 4, 'savior'),
                                       (1, 5, 'summer_garden'),
                                       (2, 1, 'skuratov'),
                                       (2, 2, 'new_holland'),
                                       (2, 3, 'sevkabel'),
                                       (2, 4, 'bolshe_coffee'),
                                       (2, 5, 'dvorcovy_bridge')) AS t(route_no, point_index, place_code)),
     ins_route_points AS (
         INSERT
             INTO route_points (id,
                                route_id,
                                place_id,
                                point_index,
                                created_at,
                                updated_at)
                 SELECT uuidv7(),
                        rm.route_id,
                        pm.place_id,
                        rps.point_index,
                        now(),
                        now()
                 FROM route_point_seed rps
                          JOIN route_map rm
                               ON rm.route_no = rps.route_no
                          JOIN place_map pm
                               ON pm.place_code = rps.place_code
                 RETURNING 1)

SELECT (SELECT count(*) FROM ins_categories)            AS inserted_place_categories,
       (SELECT count(*) FROM ins_category_translations) AS inserted_place_category_translations,
       (SELECT count(*) FROM ins_places)                AS inserted_places,
       (SELECT count(*) FROM ins_place_translations)    AS inserted_place_translations,
       (
           (SELECT count(*) FROM ins_place_primary_phones) +
           (SELECT count(*) FROM ins_place_secondary_phones)
           )                                            AS inserted_place_phones,
       (SELECT count(*) FROM ins_place_working_hours)   AS inserted_place_working_hours,
       (SELECT count(*) FROM ins_routes)                AS inserted_routes,
       (SELECT count(*) FROM ins_route_translations)    AS inserted_route_translations,
       (SELECT count(*) FROM ins_route_points)          AS inserted_route_points;
