// Vercel serverless function: returns .ics with inline disposition
// so Safari (iOS/macOS) opens Calendar app directly instead of downloading.
export default function handler(req, res) {
  const ics = (req.query && req.query.ics) || '';
  const body = Buffer.from(ics, 'utf-8');
  res.setHeader('Content-Type', 'text/calendar; charset=utf-8');
  res.setHeader('Content-Disposition', 'inline; filename="event.ics"');
  res.setHeader('Cache-Control', 'no-store');
  res.status(200).send(body);
}
