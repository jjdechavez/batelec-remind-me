import Hapi from '@hapi/hapi';
import Joi from 'joi';
import { spawn } from 'child_process'

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
    method: 'GET',
    path: '/posts',
    options: {
      handler: (request, h) => {
        let posts = []
        const fbScrape = spawn('python', ['fb-scrape.py'])
        fbScrape.stdout.on('data', (data) => {
          console.log(`stdout: ${data}`)
          // posts.push(post)
        })
        fbScrape.stderr.on('data', (data) => {
          console.log(`stderr: ${data}`)
        })
        fbScrape.on('close', (code) => {
          console.log(`child_process exited with code ${code}`)
          console.log(posts[0])
        })

        return h.response({ status: 'OK', message: 'Success get posts' }).code(200);
      },
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
      handler: (request, h) => {
        const { posts } = request.payload;
        console.log(JSON.parse(posts)[0]);

        return h.response({ status: 'ok' }).code(200);
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
