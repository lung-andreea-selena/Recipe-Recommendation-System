// src/app/app-route-reuse.strategy.ts
import { Injectable } from '@angular/core';
import {
  ActivatedRouteSnapshot,
  DetachedRouteHandle,
  RouteReuseStrategy,
} from '@angular/router';

@Injectable()
export class CacheRouteReuseStrategy implements RouteReuseStrategy {
  private storedHandles = new Map<string, DetachedRouteHandle>();

  shouldDetach(route: ActivatedRouteSnapshot): boolean {
    return route.routeConfig?.path === 'recipes';
  }

  store(route: ActivatedRouteSnapshot, handle: DetachedRouteHandle): void {
    const url = this.getRouteUrl(route);
    this.storedHandles.set(url, handle);
  }

  shouldAttach(route: ActivatedRouteSnapshot): boolean {
    const url = this.getRouteUrl(route);
    return this.storedHandles.has(url);
  }

  retrieve(route: ActivatedRouteSnapshot): DetachedRouteHandle | null {
    const url = this.getRouteUrl(route);
    return this.storedHandles.get(url) ?? null;
  }

  shouldReuseRoute(
    future: ActivatedRouteSnapshot,
    curr: ActivatedRouteSnapshot
  ): boolean {
    return future.routeConfig === curr.routeConfig;
  }

  private getRouteUrl(route: ActivatedRouteSnapshot): string {
    return route.pathFromRoot
      .map((v) => v.routeConfig?.path)
      .filter((p) => p != null)
      .join('/');
  }
}
