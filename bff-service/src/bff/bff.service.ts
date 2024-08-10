import { Injectable } from '@nestjs/common';
import { Request } from 'express';
import axios from 'axios';

@Injectable()
export class BffService {
  async proxyRequest(url: string, req: Request) {
    const method = req.method.toLowerCase();
    const data = req.body;
    const params = req.query;
    const headers = { ...req.headers };
    delete headers.host;

    const response = await axios({
      url,
      method,
      data,
      params,
      headers,
      validateStatus: function (status) {
        return status >= 200 && status < 300;
      },
      httpsAgent: new (require('https').Agent)({
        rejectUnauthorized: false,
      }),
    });

    return response;
  }
}
