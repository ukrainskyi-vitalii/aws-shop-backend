import {
  Controller,
  All,
  Get,
  Req,
  Res,
  Param,
  HttpStatus,
  Logger,
} from '@nestjs/common';
import { Request, Response } from 'express';
import { BffService } from './bff.service';
import { AxiosResponse } from 'axios';

@Controller()
export class BffController {
  private readonly logger = new Logger(BffController.name);

  constructor(private readonly bffService: BffService) {}

  @Get()
  getRoot(@Res() res: Response): void {
    res.status(HttpStatus.OK).json({ statusCode: 200, message: 'OK' });
  }

  @All(':recipientServiceName/*')
  async handleRequest(
    @Param('recipientServiceName') recipientServiceName: string,
    @Req() req: Request,
    @Res() res: Response,
  ) {
    const recipientServiceUrl = process.env[recipientServiceName.toLowerCase()];
    this.logger.log(`recipientServiceUrl: ${recipientServiceUrl}`);
    if (!recipientServiceUrl) {
      return res
        .status(HttpStatus.BAD_GATEWAY)
        .json({ error: 'Cannot process request' });
    }

    try {
      const fullUrl = `${recipientServiceUrl}${req.url.replace(`/${recipientServiceName}`, '')}`;
      this.logger.log(`Full URL: ${fullUrl}`);
      const response = await this.bffService.proxyRequest(fullUrl, req) as AxiosResponse<any>;
      res.status(response.status).json(response.data);
    } catch (error) {
      this.logger.error(
        `Error in handleRequest: ${error.message}`,
        error.stack,
      );
      if (error.response) {
        res.status(error.response.status).json(error.response.data);
      } else {
        res
          .status(HttpStatus.INTERNAL_SERVER_ERROR)
          .json({ error: 'Internal Server Error' });
      }
    }
  }
}
