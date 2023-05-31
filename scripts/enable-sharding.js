use ugc
sh.enableSharding("ugc")
db.adminCommand( { shardCollection: "ugc.view_progress", key: { film_id: "hashed" } } )
db.adminCommand( { shardCollection: "ugc.user_bookmarks", key: { film_id: "hashed" } } )
