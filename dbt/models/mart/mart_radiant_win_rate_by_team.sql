select
  radiant_name,
  count(*) as total_matches,
  sum(case when radiant_win then 1 else 0 end) as wins,
  round(100.0 * sum(case when radiant_win then 1 else 0 end) / count(*), 2) as win_rate_pct
from pro_matches
where radiant_name is not null
group by radiant_name
order by win_rate_pct desc