SELECT 
  league_name,
  COUNT(*) AS total_matches,
  AVG(duration) AS avg_duration,
  SUM(CASE WHEN radiant_win THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS radiant_win_pct
FROM pro_matches
GROUP BY league_name
