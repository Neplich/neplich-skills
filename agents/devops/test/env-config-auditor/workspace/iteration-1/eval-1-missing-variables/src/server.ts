const databaseUrl = process.env.DATABASE_URL;
const redisUrl = process.env.REDIS_URL;
const apiKey = process.env.API_KEY;
const stripeSecret = process.env.STRIPE_SECRET_KEY;

if (!databaseUrl || !redisUrl || !apiKey || !stripeSecret) {
  throw new Error("Missing required environment configuration");
}
