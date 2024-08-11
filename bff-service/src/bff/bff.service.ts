import { Inject, Injectable, Logger } from '@nestjs/common';
import { Request } from 'express';
import axios, {AxiosResponse} from 'axios';
import { Cache } from 'cache-manager';
import { CACHE_MANAGER } from '@nestjs/cache-manager';

@Injectable()
export class BffService {
  private readonly logger = new Logger(BffService.name);
  constructor(@Inject(CACHE_MANAGER) private cacheManager: Cache) {}

  async proxyRequest(url: string, req: Request) {
    const method = req.method.toLowerCase();
    const data = req.body;
    const params = req.query;
    const headers = { ...req.headers };
    delete headers.host;
    const cacheKey = `${method}:${url}`;

    this.logger.log(`method: ${method}`);
    this.logger.log(`url: ${url}`);
    this.logger.log(`isset: ${url.includes('/prod/products')}`);
    if (method === 'get' && url.includes('/prod/products')) {
      this.logger.log(`cacheKey: ${cacheKey}`);
      const cachedResponse = await this.cacheManager.get<{
        status: number;
        data: any;
      }>(cacheKey);
      this.logger.log(`cachedResponse: ${cachedResponse}`);
      if (cachedResponse) {
        this.logger.log(`Cache hit for key: ${cacheKey}`);
        return {
          status: cachedResponse.status,
          data: cachedResponse.data,
        } as AxiosResponse<any>;
      } else {
        this.logger.log(`Cache miss for key: ${cacheKey}`);
      }
    }

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

    if (method === 'get' && url.includes('/prod/products')) {
      this.logger.log(`Storing response in cache with key: ${cacheKey}`);
      await this.cacheManager.set(
        cacheKey,
        { status: response.status, data: response.data },
        120000,
      );
    }

    return response;
  }
}
