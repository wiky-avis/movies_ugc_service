use ugc
sh.enableSharding("ugc")
db.adminCommand( { shardCollection: "ugc.view_progress", key: { film_id: "hashed" } } )
db.adminCommand( { shardCollection: "ugc.user_bookmarks", key: { film_id: "hashed" } } )
db.adminCommand( { shardCollection: "ugc.user_film_reviews", key: { review_id: "hashed" } } )
db.adminCommand( { shardCollection: "ugc.film_scores", key: { film_id: "hashed" } } )
db.adminCommand( { shardCollection: "ugc.user_film_reviews_likes", key: { review_id: "hashed" } } )
