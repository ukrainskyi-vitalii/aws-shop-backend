import { Module } from '@nestjs/common';
import { BffController } from './bff.controller';
import { BffService } from './bff.service';
import { CacheModule } from '@nestjs/cache-manager';

@Module({
  imports: [
    BffModule,
    CacheModule.register({
      ttl: 120000,
      max: 10,
    }),
  ],
  controllers: [BffController],
  providers: [BffService],
})
export class BffModule {}
