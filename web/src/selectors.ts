export const qs = <T extends Element>(query: string): T | null => document.querySelector<T>(query)
export const qsa = <T extends Element>(query: string): NodeListOf<T> | null => document.querySelectorAll<T>(query)


