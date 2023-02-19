import Hapi from '@hapi/hapi';
import Joi from 'joi';

const start = async () => {
  const server = new Hapi.Server({
    debug: { request: ['error'] },
    port: 3000,
    routes: {
      cors: {
        origin: ['*'],
        credentials: true,
      },
    },
  });

  server.route({
    method: 'GET',
    path: '/',
    handler: function () {
      return 'Hello World!!';
    },
  });

  server.route({
    method: 'POST',
    path: '/posts',
    options: {
      validate: {
        options: {
          abortEarly: true,
        },
        payload: Joi.object({
          posts: Joi.string(),
        }),
      },
      handler: (request, response) => {
        const { posts } = request.payload;
        console.log(JSON.parse(posts)[0]);
        return response.response({ status: 'OK' }).code(200);
      },
    },
  });

  try {
    await server.start();
    console.log('Server running on %s', server.info.uri);
  } catch (error) {
    server.log('Error', error);
    process.exit(1);
  }
};

// Catch unhandling unexpected exceptions
process.on('uncaughtException', (error: Error) => {
  console.error(`uncaughtException ${error.message}`);
});

// Catch unhandling rejected promises
process.on('unhandledRejection', (reason: any) => {
  console.error(`unhandledRejection ${reason}`);
});

start();
