SELECT
    um.zone,
    um.region,
    r.rm_id,
    AVG(
        CASE
            -- Handle values like "13/20"
            WHEN r.score_json::jsonb
                 -> 'summery_score'
                 -> 'data'
                 ->> 'final_score' LIKE '%/%'
            THEN
                split_part(
                    r.score_json::jsonb
                    -> 'summery_score'
                    -> 'data'
                    ->> 'final_score',
                    '/',
                    1
                )::numeric
                /
                split_part(
                    r.score_json::jsonb
                    -> 'summery_score'
                    -> 'data'
                    ->> 'final_score',
                    '/',
                    2
                )::numeric

            -- Handle normal numeric values like "0.65", "78", etc.
            ELSE
                (r.score_json::jsonb
                 -> 'summery_score'
                 -> 'data'
                 ->> 'final_score')::numeric
        END
    ) AS avg_rm_score
FROM investigen.recorded_info r
JOIN investigen.user_master um
    ON r.rm_id = um.rm_id
WHERE r.score_json IS NOT NULL
  AND um.zone IS NOT NULL
  AND um.region IS NOT NULL
GROUP BY
    um.zone,
    um.region,
    r.rm_id
ORDER BY avg_rm_score DESC;