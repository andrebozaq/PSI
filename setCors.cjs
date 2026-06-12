const { Storage } = require('@google-cloud/storage');

async function configureCors() {
  const bucketName = 'psi-db-620fc.appspot.com';
  console.log('Configuring CORS for bucket:', bucketName);
  
  try {
    const storage = new Storage({ keyFilename: 'serviceAccountKey.json' });
    
    await storage.bucket(bucketName).setCorsConfiguration([
      {
        maxAgeSeconds: 3600,
        method: ['GET', 'PUT', 'POST', 'DELETE', 'OPTIONS', 'HEAD'],
        origin: ['*'],
        responseHeader: ['Content-Type', 'Authorization', 'Content-Length', 'User-Agent', 'x-goog-resumable'],
      },
    ]);

    console.log(`Success! Bucket ${bucketName} was updated with a CORS config to allow all origins.`);
  } catch (error) {
    console.error('Error configuring CORS:', error);
  }
}

configureCors();
