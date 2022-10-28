SELECT
  month,
  COUNT(*) AS list_count
FROM (
  SELECT DISTINCT
    min(to_char(l.created_at, 'YYYY-MM')) AS month,
    c.id
  FROM api_facilitylist l
  JOIN api_source s ON s.facility_list_id = l.id
  JOIN api_contributor c ON s.contributor_id = c.id
  JOIN api_user u ON u.id = c.admin_id
  WHERE to_char(l.created_at, 'YYYY-MM') != to_char(now(), 'YYYY-MM')
  AND (u.email LIKE '%openapparel.org%' OR u.email LIKE '%opensupplyhub.org%')
  GROUP BY c.id
) s
GROUP BY month
ORDER BY month;
